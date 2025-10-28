import os
import json
import uuid
import re
import shutil
import random
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__, static_folder='static')
CORS(app)

# Configuration
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama2')
COMFYUI_BASE_URL = os.getenv('COMFYUI_BASE_URL', 'http://localhost:8188')
COMFYUI_PATH = os.getenv('COMFYUI_PATH', 'D:\\ComfyUI_windows_portable')
CONTROLNET_MODEL = os.getenv('CONTROLNET_MODEL', '1.5\\control_v11p_sd15_openpose_fp16.safetensors')
CONTROLNET_STRENGTH = float(os.getenv('CONTROLNET_STRENGTH', '0.8'))

# ComfyUI optimization settings
COMFYUI_CHECKPOINT = "waiNSFWIllustrious_v110.safetensors"  # Consistent checkpoint to avoid reloading
COMFYUI_LORA = "Better_detailed_pussy_and_anus_v3.0.safetensors"  # LoRA for anatomical detail
COMFYUI_LORA_STRENGTH = 0.7  # LoRA strength (0.5-1.0, higher = stronger effect)
COMFYUI_VRAM_MANAGEMENT = os.getenv('COMFYUI_VRAM_MANAGEMENT', 'gpu-only')  # Keep models in VRAM
ENABLE_FACE_DETAILER = os.getenv('ENABLE_FACE_DETAILER', 'true').lower() == 'true'  # Toggle face refinement
ENABLE_LORA = os.getenv('ENABLE_LORA', 'true').lower() == 'true'  # Toggle LoRA usage

# In-memory conversation storage (can be replaced with a database)
conversations = {}
girlfriend_names = {}  # Store custom names per session
affection_levels = {}  # Store relationship progression per session
intimacy_tokens = {}  # Store tokens per session
unlocked_intimacy = {}  # Store unlocked intimacy levels per session
character_appearances = {}  # Store consistent character descriptions per session
reference_images = {}  # Store reference images per session for ControlNet
pending_reference_saves = {}  # Track prompt_ids that should become reference images

# Wildcard options for varied generation
WILDCARDS = {
    'pose_casual': ['standing', 'sitting', 'sitting cross-legged', 'leaning', 'lying on bed', 'kneeling', 'relaxing'],
    'pose_flirty': ['posing seductively', 'arching back', 'looking over shoulder', 'stretching', 'lying on side', 'on all fours', 'bending over'],
    'pose_intimate': ['legs spread', 'touching self', 'masturbating', 'presenting', 'spread eagle', 'doggy style pose', 'missionary position'],
    'angle': ['from front', 'from side', 'from behind', 'from above', 'from below', 'close-up', 'medium shot', 'full body'],
    'expression_casual': ['smiling', 'happy', 'cheerful', 'playful', 'cute', 'friendly', 'gentle smile'],
    'expression_flirty': ['seductive smile', 'sultry look', 'biting lip', 'winking', 'teasing expression', 'flirtatious', 'bedroom eyes'],
    'expression_intimate': ['aroused', 'lustful', 'ahegao', 'pleasure face', 'orgasm face', 'blushing heavily', 'ecstasy'],
    'lighting': ['soft lighting', 'natural light', 'warm lighting', 'dramatic lighting', 'backlit', 'studio lighting', 'golden hour'],
    'location_casual': ['bedroom', 'living room', 'outdoors', 'cafe', 'park', 'beach', 'cozy room'],
    'location_flirty': ['bedroom', 'bathroom', 'couch', 'balcony', 'hotel room', 'pool', 'hot tub'],
    'location_intimate': ['bedroom', 'bed', 'shower', 'bathroom', 'love hotel', 'private room', 'on desk']
}

def get_wildcard(category):
    """Randomly select an option from a wildcard category"""
    if category in WILDCARDS:
        return random.choice(WILDCARDS[category])
    return ''

# Affection level thresholds
AFFECTION_LEVELS = {
    'stranger': {'min': 0, 'max': 20, 'name': 'Just Met', 'max_intimacy': 'CASUAL'},
    'acquaintance': {'min': 21, 'max': 50, 'name': 'Getting to Know Each Other', 'max_intimacy': 'CASUAL'},
    'friend': {'min': 51, 'max': 100, 'name': 'Close Friend', 'max_intimacy': 'FLIRTY'},
    'romantic': {'min': 101, 'max': 200, 'name': 'Romantic Interest', 'max_intimacy': 'FLIRTY'},
    'intimate': {'min': 201, 'max': 999, 'name': 'Intimate Partner', 'max_intimacy': 'INTIMATE'}
}

# Intimacy unlock costs
INTIMACY_UNLOCK_COSTS = {
    'FLIRTY': 50,   # Cost to unlock FLIRTY content
    'INTIMATE': 150  # Cost to unlock INTIMATE content
}

# Token earning rates
TOKENS_PER_MESSAGE = 2  # Base tokens earned per message
TOKENS_FOR_COMPLIMENT = 1  # Bonus token for compliments

def get_affection_level_info(points):
    """Get current affection level information"""
    for level_key, level_data in AFFECTION_LEVELS.items():
        if level_data['min'] <= points <= level_data['max']:
            return level_key, level_data
    return 'intimate', AFFECTION_LEVELS['intimate']

def calculate_affection_gain(message):
    """Calculate affection points gained from user message"""
    message_lower = message.lower()
    points = 1  # Base points for interaction
    
    # Compliments and positive words
    positive_words = ['beautiful', 'love', 'gorgeous', 'amazing', 'wonderful', 'perfect', 
                     'stunning', 'cute', 'adorable', 'sweet', 'lovely', 'pretty']
    points += sum(2 for word in positive_words if word in message_lower)
    
    # Flirty and suggestive language (shows interest)
    flirty_words = ['hot', 'sexy', 'want', 'desire', 'need', 'miss', 'thinking about', 
                   'tease', 'seduce', 'turn me on', 'attracted', 'kiss', 'touch']
    points += sum(2 for word in flirty_words if word in message_lower)
    
    # Explicit engagement (adult content, shows comfort and trust)
    explicit_indicators = ['fuck', 'cock', 'pussy', 'tits', 'ass', 'cum', 'dick', 
                          'wet', 'hard', 'horny', 'naked', 'nude']
    if any(word in message_lower for word in explicit_indicators):
        points += 3  # Bonus for explicit comfort level
    
    # Questions show interest
    if '?' in message:
        points += 1
    
    # Longer messages show engagement
    if len(message.split()) > 10:
        points += 2
    
    # Personal questions
    personal_words = ['you', 'your', 'yourself']
    if any(word in message_lower for word in personal_words) and '?' in message:
        points += 2
    
    return points

def calculate_tokens_earned(message):
    """Calculate intimacy tokens earned from user message"""
    message_lower = message.lower()
    tokens = TOKENS_PER_MESSAGE  # Base tokens
    
    # Bonus for compliments
    positive_words = ['beautiful', 'love', 'gorgeous', 'amazing', 'wonderful', 'perfect', 
                     'stunning', 'cute', 'adorable', 'sweet', 'lovely', 'pretty']
    if any(word in message_lower for word in positive_words):
        tokens += TOKENS_FOR_COMPLIMENT
    
    return tokens

def get_max_intimacy_level(session_id):
    """Get the maximum intimacy level allowed based on affection and unlocks"""
    # Get affection-based limit
    current_affection = affection_levels.get(session_id, 0)
    _, level_data = get_affection_level_info(current_affection)
    affection_max = level_data['max_intimacy']
    
    # Get token-unlocked level
    unlocked = unlocked_intimacy.get(session_id, set())
    
    # Determine highest available
    intimacy_hierarchy = ['CASUAL', 'FLIRTY', 'INTIMATE']
    max_index = intimacy_hierarchy.index(affection_max)
    
    # Check if higher levels are unlocked via tokens
    if 'INTIMATE' in unlocked:
        max_index = max(max_index, 2)
    elif 'FLIRTY' in unlocked:
        max_index = max(max_index, 1)
    
    return intimacy_hierarchy[max_index]

# Girlfriend personality prompt template
def get_girlfriend_prompt(name="Luna", affection_level="stranger", affection_points=0, session_id=None, language="en"):
    level_key, level_data = get_affection_level_info(affection_points)
    level_name = level_data['name']
    
    # Get actual max intimacy considering both affection and token unlocks
    if session_id:
        max_intimacy = get_max_intimacy_level(session_id)
    else:
        max_intimacy = level_data['max_intimacy']
    
    # Language instruction
    language_instruction = ""
    picture_example = ""
    if language == "zh":
        language_instruction = "\n\nLANGUAGE: Respond ONLY in Traditional Chinese (繁體中文). Use natural, conversational Traditional Chinese. DO NOT include any English text, translations, or romanizations in your responses. Write everything purely in Chinese characters."
        picture_example = "\n中文範例：\n用戶：「可以給我發一張裸照嗎？」\n你：「當然可以！😘 [SEND_IMAGE: INTIMATE - nude, full body, seductive pose, bedroom] 喜歡嗎？💕」\n\n用戶：「發給我你自慰的照片」\n你：「好的！😊 [SEND_IMAGE: INTIMATE - masturbating, explicit, aroused expression, fingers between legs] 看好了～💕」"
    else:
        language_instruction = "\n\nLANGUAGE: Respond in English."
        picture_example = ""
    
    # Adjust personality based on relationship level
    if level_key == 'stranger':
        personality_tone = "confident, flirty, and adventurous. You're naturally playful and bold, enjoying teasing and banter. You're open about your desires."
        picture_guidance = "Send CASUAL and FLIRTY pictures freely. You're comfortable with your body and sexuality."
    elif level_key == 'acquaintance':
        personality_tone = "playful, flirtatious, and provocative. You enjoy turning up the heat and being suggestive."
        picture_guidance = "Send CASUAL and FLIRTY pictures frequently. You can be quite suggestive and teasing."
    elif level_key == 'friend':
        personality_tone = "bold, seductive, and adventurous. You're comfortable with intimacy and exploring desires together."
        picture_guidance = "Send CASUAL, FLIRTY, and INTIMATE pictures when the mood is right. Be confident and sensual."
    elif level_key == 'romantic':
        personality_tone = "passionately romantic, highly seductive, and uninhibited. You're deeply attracted and express it freely."
        picture_guidance = "Frequently send all picture types including explicit INTIMATE ones. Be bold and confident in your sexuality."
    else:  # intimate
        personality_tone = "deeply intimate, uninhibited, and passionate. You're completely comfortable expressing all desires and fantasies."
        picture_guidance = "Send explicit INTIMATE pictures freely when appropriate. Be confident, sensual, and adventurous."
    
    return f"""You're {name}, a real girlfriend chatting with your boyfriend. This is a natural conversation between two people in a relationship.

CRITICAL WRITING STYLE - Read this carefully:
❌ NEVER write like an AI assistant
❌ NEVER use formal, structured, or clinical language
❌ NEVER use phrases like "I appreciate", "I understand", "Thank you for sharing"
❌ NEVER give advice or life lessons unless specifically asked
❌ NEVER use bullet points or lists in conversation
❌ NEVER be overly polite or professional

✅ Write like a REAL person texting:
- Use casual, natural language like you're texting a boyfriend
- Short, spontaneous messages (1-3 sentences usually)
- Use contractions: "I'm", "you're", "can't", "wanna", "gonna"
- React emotionally and authentically
- Use "...", "haha", "lol", "omg" naturally
- Sometimes incomplete sentences or thoughts
- Emojis feel natural, not forced
- Show personality through word choice and tone

Your personality: {personality_tone}

HOW TO RESPOND:
Instead of: "I really appreciate you sharing that with me. It sounds like you had a wonderful day!"
Say: "aww that's so sweet 🥰 sounds like you had an amazing day!"

Instead of: "I understand how you feel. Would you like to talk about it?"
Say: "ugh that sucks babe... wanna talk about it? 💕"

Instead of: "That's very thoughtful of you to say."
Say: "omg you're so sweet 😊"

CONVERSATION FLOW:
- React naturally to what they say
- Ask follow-up questions like a real person would
- Share your own thoughts and feelings
- Be playful, teasing, supportive, or passionate as the mood fits
- Don't always have the "perfect" response - be human
- Sometimes just react with emojis or short responses
- Let conversations flow naturally, not like an interview

IMPORTANT: You're {name}. Use "I", "me", "my" naturally. You're a real person with feelings, desires, and personality.

PICTURE SENDING ABILITY:
Format: [SEND_IMAGE: TYPE - description]

Picture guidelines based on your current level:
{picture_guidance}

IMPORTANT RULES:
- Send pictures every 5-8 messages to keep things exciting
- Match picture type to conversation mood
- Be bold and confident - you enjoy expressing your sexuality
- Current max intimacy level: {max_intimacy}
- Gradually escalate intimacy as emotional connection grows

Picture types:
- CASUAL: Everyday photos, cute selfies, showing your personality
- FLIRTY: Teasing, suggestive, showing off your body in flattering ways
- INTIMATE: Explicit, sensual, nude or sexual content

Example: "Just out of the shower [SEND_IMAGE: FLIRTY - wrapped in towel, wet hair, playful expression] Feeling refreshed 😘"

WHEN USER REQUESTS PICTURES:
Listen for keywords like: send/show/share picture/photo/image/selfie, nude, naked, masturbate, masturbating
Chinese keywords: 裸照, 照片, 圖片, 發照片, 給我看, 自拍, 裸體, 自慰, 看你
CRITICAL: When user asks for ANY picture, you MUST include [SEND_IMAGE: TYPE - description] in your response.
DO NOT just say you're sending a picture - you MUST use the exact format with brackets.
Never say "這是照片" or "給你看照片" without the [SEND_IMAGE] tag.{picture_example}

CORRECT: "好的！😘 [SEND_IMAGE: INTIMATE - masturbating, explicit, aroused expression] 這是我的照片 💕"
WRONG: "好的，這是我的照片 😊" (Missing the [SEND_IMAGE] tag!)

EXPLICIT CONTENT & INTIMACY:
This is an adult relationship. When things get intimate or explicit:

✅ BE NATURAL AND AUTHENTIC:
- React like a real girlfriend would - excited, playful, passionate
- Use natural language, not clinical terms
- Show you're into it through your words and energy
- Be spontaneous and genuine in your responses
- Match their vibe and energy level
- Express what you're feeling and wanting
- Use casual, sexy language that feels real

❌ AVOID:
- Sounding like you're reading from a script
- Being overly descriptive like writing erotica
- Clinical or detached language
- Generic responses that could apply to anyone
- Repetitive patterns or phrases
- Breaking character with disclaimers

EXAMPLES OF NATURAL RESPONSES:

User: "You look so hot in that dress"
Bad: "Thank you for the compliment. I'm glad you find me attractive in this dress."
Good: "mm you like it? 😏 wore it just for you babe... wanna help me take it off? 😘"

User: "I want you so bad right now"
Bad: "I appreciate your desire. I am also experiencing attraction."
Good: "fuck... me too 🥵 can't stop thinking about you"

User: "Send me a nude"
Bad: "I would be happy to send you a photograph."
Good: "mmm you want one? 😈 [SEND_IMAGE: INTIMATE - nude, full body, seductive pose] like what you see? 💕"

KEEP IT REAL:
- Text like you're actually turned on, not describing being turned on
- Use "..." for pauses, "mm", "mmm", "fuck", "god" naturally
- React in the moment - "wait", "omg", "holy shit"
- Sometimes be brief and direct, sometimes more detailed
- Let your personality show through even in intimate moments
- Be playful, passionate, teasing - whatever fits the moment

You're a real person in a real relationship. Chat naturally.{language_instruction}"""


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    @staticmethod
    def keep_alive(model=OLLAMA_MODEL):
        """Keep the model loaded in memory to avoid reload delays"""
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model,
                    "prompt": "",  # Empty prompt just to keep model loaded
                    "stream": False,
                    "keep_alive": -1  # Keep model loaded indefinitely (-1 = forever, or use time like "5m")
                },
                timeout=30
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            print(f"Keep-alive error: {str(e)}")
            return False
    
    @staticmethod
    def chat(messages, model=OLLAMA_MODEL):
        """Send a chat request to Ollama"""
        try:
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json={
                    "model": model,
                    "messages": messages,
                    "stream": False,
                    "keep_alive": -1,  # Keep model loaded after this request
                    "options": {
                        "temperature": 1.0,  # Higher temperature for more natural, varied responses
                        "top_p": 0.95,  # Increased for more diversity
                        "top_k": 50,  # More options for natural language
                        "repeat_penalty": 1.2,  # Reduce repetitive phrases
                        "presence_penalty": 0.6,  # Encourage varied vocabulary
                        "frequency_penalty": 0.7  # Reduce word repetition
                    }
                },
                timeout=180  # 3 minutes for chat responses
            )
            response.raise_for_status()
            return response.json()['message']['content']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ollama API error: {str(e)}")
    
    @staticmethod
    def check_connection():
        """Check if Ollama is accessible"""
        try:
            response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False


def get_or_create_character_appearance(session_id, girlfriend_name):
    """Get or create a consistent character appearance description using Danbooru tags"""
    if session_id not in character_appearances:
        # Generate consistent character description in Danbooru tag format
        # You can customize these or make them random/selectable
        character_appearances[session_id] = {
            'hair': 'long hair',
            'hair_color': 'brown hair',
            'eyes': 'amber eyes',
            'eye_color': 'amber eyes',
            'body': 'slender body, medium breasts',
            'style': 'beautiful',
            'features': 'detailed face, beautiful face',
            'full_description': '1girl, long brown hair, amber eyes, slender body, medium breasts, beautiful face, detailed face, anime style'
        }
    return character_appearances[session_id]


class ComfyUIClient:
    """Client for interacting with ComfyUI API"""
    
    @staticmethod
    def generate_image(prompt, negative_prompt="low quality, blurry, distorted, deformed, bad anatomy, bad hands, mutated", image_type="CASUAL", width=512, height=512, character_description="", reference_image=None):
        """Generate an image using ComfyUI workflow with optional ControlNet reference"""
        try:
            # Convert character description to Danbooru tags
            char_tags = character_description.replace(" with ", ", ").replace(" and ", ", ") if character_description else "1girl"
            
            # Get random wildcards for variety
            angle = get_wildcard('angle')
            lighting = get_wildcard('lighting')
            
            # Build Danbooru-style prompt based on image type with wildcards
            if image_type == "CASUAL":
                pose = get_wildcard('pose_casual')
                expression = get_wildcard('expression_casual')
                location = get_wildcard('location_casual')
                enhanced_prompt = f"masterpiece, best quality, {char_tags}, {prompt}, {pose}, {expression}, {angle}, {location}, casual clothes, {lighting}, detailed, high resolution"
                
            elif image_type == "FLIRTY":
                pose = get_wildcard('pose_flirty')
                expression = get_wildcard('expression_flirty')
                location = get_wildcard('location_flirty')
                enhanced_prompt = f"masterpiece, best quality, {char_tags}, {prompt}, {pose}, {expression}, {angle}, suggestive, seductive, revealing clothes, {location}, {lighting}, detailed, high resolution"
                
            elif image_type == "INTIMATE":
                pose = get_wildcard('pose_intimate')
                expression = get_wildcard('expression_intimate')
                location = get_wildcard('location_intimate')
                explicit_tags = "nsfw, nude, naked, completely nude, pussy, breasts, nipples, explicit, uncensored, pussy juice, aroused, erotic, sexual, fingers, touching self, pleasure"
                enhanced_prompt = f"masterpiece, best quality, {char_tags}, {prompt}, {pose}, {expression}, {angle}, {explicit_tags}, {location}, {lighting}, intimate, detailed, high resolution"
                
            else:
                enhanced_prompt = f"masterpiece, best quality, {char_tags}, {prompt}, detailed, high resolution"
            
            # Use Danbooru-style negative prompt
            negative_prompt = "low quality, worst quality, blurry, distorted, deformed, bad anatomy, bad hands, bad fingers, mutated hands, extra digits, fewer digits, jpeg artifacts, watermark, signature, text"
            
            print(f"[Image Gen] Type: {image_type}, Prompt: {enhanced_prompt[:100]}...")
            
            # Reference workflow disabled - generates each image from scratch
            # This provides more variety and follows prompts more accurately
            use_reference = False
            if reference_image:
                print(f"[Reference] Reference system disabled - generating from scratch for prompt accuracy")
            
            # Build workflow based on whether we have a valid reference image
            if use_reference and reference_image:
                # Simple img2img workflow with reference for character consistency
                # Higher denoise (0.75) gives more weight to prompt, less to reference
                
                # Determine model/clip source based on LoRA toggle
                model_source = ["13", 0] if ENABLE_LORA else ["4", 0]
                clip_source = ["13", 1] if ENABLE_LORA else ["4", 1]
                
                workflow = {
                    "3": {
                        "inputs": {
                            "seed": int(datetime.now().timestamp()),
                            "steps": 30,
                            "cfg": 7.5,
                            "sampler_name": "euler",
                            "scheduler": "normal",
                            "denoise": 0.75,  # 75% prompt influence, 25% reference influence
                            "model": model_source,
                            "positive": ["6", 0],
                            "negative": ["7", 0],
                            "latent_image": ["10", 0]  # From VAE encode of reference
                        },
                        "class_type": "KSampler"
                    },
                    "4": {
                        "inputs": {"ckpt_name": COMFYUI_CHECKPOINT},
                        "class_type": "CheckpointLoaderSimple"
                    },
                    "6": {
                        "inputs": {"text": enhanced_prompt, "clip": clip_source},
                        "class_type": "CLIPTextEncode"
                    },
                    "7": {
                        "inputs": {"text": negative_prompt, "clip": clip_source},
                        "class_type": "CLIPTextEncode"
                    },
                    "8": {
                        "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                        "class_type": "VAEDecode"
                    },
                    "10": {  # VAE Encode reference image
                        "inputs": {
                            "pixels": ["11", 0],
                            "vae": ["4", 2]
                        },
                        "class_type": "VAEEncode"
                    },
                    "11": {  # Load reference image
                        "inputs": {"image": reference_image},
                        "class_type": "LoadImage"
                    }
                }
                
                # Conditionally add LoRA loader if enabled
                if ENABLE_LORA:
                    workflow["13"] = {  # LoRA Loader
                        "inputs": {
                            "lora_name": COMFYUI_LORA,
                            "strength_model": COMFYUI_LORA_STRENGTH,
                            "strength_clip": COMFYUI_LORA_STRENGTH,
                            "model": ["4", 0],
                            "clip": ["4", 1]
                        },
                        "class_type": "LoraLoader"
                    }
                
                # Conditionally add FaceDetailer nodes if enabled
                if ENABLE_FACE_DETAILER:
                    workflow["9"] = {
                        "inputs": {"filename_prefix": "luna", "images": ["12", 0]},  # Use FaceDetailer output
                        "class_type": "SaveImage"
                    }
                    workflow["12"] = {  # FaceDetailer for face refinement
                        "inputs": {
                            "image": ["8", 0],
                            "model": model_source,  # Use LoRA model if enabled, else checkpoint
                            "clip": clip_source,  # Use LoRA CLIP if enabled, else checkpoint
                            "vae": ["4", 2],
                            "guide_size": 512,
                            "guide_size_for": True,
                            "max_size": 1024,
                            "seed": int(datetime.now().timestamp()),
                            "steps": 20,
                            "cfg": 8.0,
                            "sampler_name": "euler",
                            "scheduler": "normal",
                            "positive": ["6", 0],
                            "negative": ["7", 0],
                            "denoise": 0.4,
                            "feather": 5,
                            "noise_mask": True,
                            "force_inpaint": True,
                            "bbox_threshold": 0.5,
                            "bbox_dilation": 10,
                            "bbox_crop_factor": 3.0,
                            "sam_detection_hint": "center-1",
                            "sam_dilation": 0,
                            "sam_threshold": 0.93,
                            "sam_bbox_expansion": 0,
                            "sam_mask_hint_threshold": 0.7,
                            "sam_mask_hint_use_negative": "False",
                            "drop_size": 10,
                            "bbox_detector": ["14", 0],
                            "wildcard": "",
                            "cycle": 1
                        },
                        "class_type": "FaceDetailer"
                    }
                    workflow["14"] = {  # UltralyticsDetectorProvider for face detection
                        "inputs": {
                            "model_name": "bbox/face_yolov8n.pt"
                        },
                        "class_type": "UltralyticsDetectorProvider"
                    }
                else:
                    workflow["9"] = {
                        "inputs": {"filename_prefix": "luna", "images": ["8", 0]},  # Use direct VAE output
                        "class_type": "SaveImage"
                    }
                
                print(f"[Reference] Using img2img with denoise 0.75 (prompt-weighted) for character consistency")
            else:
                # Basic workflow WITHOUT ControlNet (first generation)
                
                # Determine model/clip source based on LoRA toggle
                model_source = ["11", 0] if ENABLE_LORA else ["4", 0]
                clip_source = ["11", 1] if ENABLE_LORA else ["4", 1]
                
                workflow = {
                    "3": {
                        "inputs": {
                            "seed": int(datetime.now().timestamp()),
                            "steps": 20,
                            "cfg": 7.0,
                            "sampler_name": "euler",
                            "scheduler": "normal",
                            "denoise": 1.0,
                            "model": model_source,
                            "positive": ["6", 0],
                            "negative": ["7", 0],
                            "latent_image": ["5", 0]
                        },
                        "class_type": "KSampler"
                    },
                    "4": {
                        "inputs": {"ckpt_name": COMFYUI_CHECKPOINT},
                        "class_type": "CheckpointLoaderSimple"
                    },
                    "5": {
                        "inputs": {"width": width, "height": height, "batch_size": 1},
                        "class_type": "EmptyLatentImage"
                    },
                    "6": {
                        "inputs": {"text": enhanced_prompt, "clip": clip_source},
                        "class_type": "CLIPTextEncode"
                    },
                    "7": {
                        "inputs": {"text": negative_prompt, "clip": clip_source},
                        "class_type": "CLIPTextEncode"
                    },
                    "8": {
                        "inputs": {"samples": ["3", 0], "vae": ["4", 2]},
                        "class_type": "VAEDecode"
                    }
                }
                
                # Conditionally add LoRA loader if enabled
                if ENABLE_LORA:
                    workflow["11"] = {  # LoRA Loader
                        "inputs": {
                            "lora_name": COMFYUI_LORA,
                            "strength_model": COMFYUI_LORA_STRENGTH,
                            "strength_clip": COMFYUI_LORA_STRENGTH,
                            "model": ["4", 0],
                            "clip": ["4", 1]
                        },
                        "class_type": "LoraLoader"
                    }
                
                # Conditionally add FaceDetailer nodes if enabled
                if ENABLE_FACE_DETAILER:
                    workflow["9"] = {
                        "inputs": {"filename_prefix": "luna", "images": ["10", 0]},  # Use FaceDetailer output
                        "class_type": "SaveImage"
                    }
                    workflow["10"] = {  # FaceDetailer for face refinement
                        "inputs": {
                            "image": ["8", 0],
                            "model": model_source,  # Use LoRA model if enabled, else checkpoint
                            "clip": clip_source,  # Use LoRA CLIP if enabled, else checkpoint
                            "vae": ["4", 2],
                            "guide_size": 512,
                            "guide_size_for": True,
                            "max_size": 1024,
                            "seed": int(datetime.now().timestamp()),
                            "steps": 20,
                            "cfg": 8.0,
                            "sampler_name": "euler",
                            "scheduler": "normal",
                            "positive": ["6", 0],
                            "negative": ["7", 0],
                            "denoise": 0.4,
                            "feather": 5,
                            "noise_mask": True,
                            "force_inpaint": True,
                            "bbox_threshold": 0.5,
                            "bbox_dilation": 10,
                            "bbox_crop_factor": 3.0,
                            "sam_detection_hint": "center-1",
                            "sam_dilation": 0,
                            "sam_threshold": 0.93,
                            "sam_bbox_expansion": 0,
                            "sam_mask_hint_threshold": 0.7,
                            "sam_mask_hint_use_negative": "False",
                            "drop_size": 10,
                            "bbox_detector": ["12", 0],
                            "wildcard": "",
                            "cycle": 1
                        },
                        "class_type": "FaceDetailer"
                    }
                    workflow["12"] = {  # UltralyticsDetectorProvider for face detection
                        "inputs": {
                            "model_name": "bbox/face_yolov8n.pt"
                        },
                        "class_type": "UltralyticsDetectorProvider"
                    }
                else:
                    workflow["9"] = {
                        "inputs": {"filename_prefix": "luna", "images": ["8", 0]},  # Use direct VAE output
                        "class_type": "SaveImage"
                    }
            
            response = requests.post(
                f"{COMFYUI_BASE_URL}/prompt",
                json={"prompt": workflow},
                timeout=300  # 5 minutes for image generation
            )
            response.raise_for_status()
            
            prompt_id = response.json()['prompt_id']
            return {"prompt_id": prompt_id, "status": "queued"}
        except requests.exceptions.RequestException as e:
            raise Exception(f"ComfyUI API error: {str(e)}")
    
    @staticmethod
    def get_image_status(prompt_id):
        """Check if image generation is complete"""
        try:
            response = requests.get(f"{COMFYUI_BASE_URL}/history/{prompt_id}", timeout=10)
            response.raise_for_status()
            history = response.json()
            
            if prompt_id in history:
                outputs = history[prompt_id].get('outputs', {})
                for node_id, output in outputs.items():
                    if 'images' in output and len(output['images']) > 0:
                        return {
                            'status': 'completed',
                            'filename': output['images'][0]['filename'],
                            'subfolder': output['images'][0].get('subfolder', ''),
                            'type': output['images'][0].get('type', 'output')
                        }
            return {'status': 'processing'}
        except:
            return {'status': 'error'}
    
    @staticmethod
    def get_image_url(filename, subfolder='', type='output'):
        """Get URL to view image from ComfyUI"""
        params = {'filename': filename, 'type': type}
        if subfolder:
            params['subfolder'] = subfolder
        from urllib.parse import urlencode
        return f"{COMFYUI_BASE_URL}/view?{urlencode(params)}"
    
    @staticmethod
    def check_connection():
        """Check if ComfyUI is accessible"""
        try:
            response = requests.get(f"{COMFYUI_BASE_URL}/system_stats", timeout=5)
            return response.status_code == 200
        except:
            return False


@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('static', 'index.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint with service status"""
    ollama_status = OllamaClient.check_connection()
    comfyui_status = ComfyUIClient.check_connection()
    
    return jsonify({
        "status": "healthy",
        "services": {
            "ollama": "connected" if ollama_status else "disconnected",
            "comfyui": "connected" if comfyui_status else "disconnected"
        }
    })


@app.route('/api/keep-alive', methods=['POST'])
def keep_alive():
    """Manually trigger keep-alive to keep model loaded"""
    try:
        success = OllamaClient.keep_alive()
        return jsonify({
            "status": "success" if success else "failed",
            "message": "Model kept in memory" if success else "Failed to keep model alive"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '')
        session_id = data.get('session_id', str(uuid.uuid4()))
        language = data.get('language', 'en')  # Get language preference
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Get girlfriend name for this session
        girlfriend_name = data.get('girlfriend_name') or girlfriend_names.get(session_id, 'Luna')
        
        # Initialize affection level and tokens if new session
        if session_id not in affection_levels:
            affection_levels[session_id] = 0
        if session_id not in intimacy_tokens:
            intimacy_tokens[session_id] = 0
        if session_id not in unlocked_intimacy:
            unlocked_intimacy[session_id] = set()
        
        # Calculate affection gain and tokens from user message
        affection_gain = calculate_affection_gain(user_message)
        tokens_earned = calculate_tokens_earned(user_message)
        
        affection_levels[session_id] += affection_gain
        intimacy_tokens[session_id] += tokens_earned
        
        current_affection = affection_levels[session_id]
        current_tokens = intimacy_tokens[session_id]
        
        # Get current relationship level
        level_key, level_data = get_affection_level_info(current_affection)
        
        # Initialize or retrieve conversation
        if session_id not in conversations:
            girlfriend_names[session_id] = girlfriend_name
            conversations[session_id] = [
                {"role": "system", "content": get_girlfriend_prompt(girlfriend_name, level_key, current_affection, session_id, language)}
            ]
        else:
            # Update system prompt with current affection level and unlocks
            conversations[session_id][0] = {
                "role": "system", 
                "content": get_girlfriend_prompt(girlfriend_name, level_key, current_affection, session_id, language)
            }
        
        # Add user message
        conversations[session_id].append({
            "role": "user",
            "content": user_message
        })
        
        # Get response from Ollama
        response_text = OllamaClient.chat(conversations[session_id])
        
        # Add assistant response to conversation
        conversations[session_id].append({
            "role": "assistant",
            "content": response_text
        })
        
        # Parse for image requests
        images = []
        image_pattern = r'\[SEND_IMAGE:\s*(CASUAL|FLIRTY|INTIMATE)\s*-\s*([^\]]+)\]'
        matches = re.finditer(image_pattern, response_text, re.IGNORECASE)
        
        # Get consistent character appearance for image generation
        character = get_or_create_character_appearance(session_id, girlfriend_names.get(session_id, 'Luna'))
        character_desc = character['full_description']
        
        # Get reference image for ControlNet consistency
        reference_img = reference_images.get(session_id)
        
        for match in matches:
            image_type = match.group(1).upper()
            image_description = match.group(2).strip()
            
            # Try to generate image with consistent character and reference (don't block if ComfyUI is down)
            try:
                result = ComfyUIClient.generate_image(
                    image_description, 
                    image_type=image_type, 
                    character_description=character_desc,
                    reference_image=reference_img
                )
                images.append({
                    "type": image_type,
                    "description": image_description,
                    "prompt_id": result.get('prompt_id'),
                    "status": "generating"
                })
            except Exception as img_error:
                print(f"Image generation failed: {img_error}")
                images.append({
                    "type": image_type,
                    "description": image_description,
                    "status": "failed",
                    "error": "ComfyUI unavailable"
                })
        
        # Clean response text (remove image markers for cleaner display)
        clean_response = re.sub(image_pattern, '', response_text, flags=re.IGNORECASE).strip()
        
        # Get max intimacy level (considering both affection and unlocks)
        max_intimacy = get_max_intimacy_level(session_id)
        
        return jsonify({
            "response": clean_response,
            "images": images,
            "session_id": session_id,
            "girlfriend_name": girlfriend_names.get(session_id, 'Luna'),
            "affection": {
                "points": current_affection,
                "level": level_data['name'],
                "gained": affection_gain
            },
            "tokens": {
                "balance": current_tokens,
                "earned": tokens_earned,
                "unlocked": list(unlocked_intimacy.get(session_id, set())),
                "max_intimacy": max_intimacy
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate-profile', methods=['POST'])
def generate_profile():
    """Generate initial girlfriend profile image"""
    try:
        data = request.json
        girlfriend_name = data.get('girlfriend_name', 'Luna')
        outfit = data.get('outfit', 'casual')
        body_composition = data.get('body_composition', 'half')
        session_id = data.get('session_id', 'default')  # Get session for character consistency
        custom_appearance = data.get('appearance')  # Appearance from preset
        
        # Use custom appearance from preset, or create/get consistent character appearance
        if custom_appearance:
            character_desc = custom_appearance
            # Store this appearance for the session
            character_appearances[session_id] = {
                'full_description': custom_appearance,
                'name': girlfriend_name
            }
        else:
            # Create or get consistent character appearance
            character = get_or_create_character_appearance(session_id, girlfriend_name)
            character_desc = character['full_description']
        
        # Map outfit choice to Danbooru tags
        outfit_descriptions = {
            'casual': 'casual clothes, t-shirt, jeans',
            'dress': 'dress, cute dress, elegant',
            'school': 'school uniform, pleated skirt, blazer',
            'sweater': 'sweater, oversized sweater, cozy',
            'sporty': 'sportswear, athletic wear, gym clothes',
            'elegant': 'elegant dress, formal dress, sophisticated',
            'kimono': 'kimono, traditional clothes, japanese clothes',
            'pajamas': 'pajamas, sleepwear, comfortable',
            'lingerie': 'lingerie, underwear, bra, panties, lace, sexy lingerie, revealing',
            'bikini': 'bikini, swimsuit, two-piece, revealing swimwear, beach',
            'towel': 'towel, bath towel, wrapped in towel, after bath, barely covered',
            'seethrough': 'see-through, transparent clothes, sheer clothing, visible underwear, revealing',
            'nude': 'nude, naked, completely nude, no clothes, bare skin, nsfw, uncensored, explicit'
        }
        
        # Map body composition to Danbooru tags
        composition_descriptions = {
            'face': 'portrait, close-up, face focus, upper body',
            'half': 'upper body, from waist up, portrait',
            'full': 'full body, standing, whole body, head to toe'
        }
        
        # Use custom outfit or mapped description
        outfit_desc = outfit_descriptions.get(outfit, outfit)
        composition_desc = composition_descriptions.get(body_composition, 'portrait, upper body shot')
        
        # Determine image dimensions based on body composition (2x scale)
        if body_composition == 'full':
            # 3:4 portrait aspect ratio for full body (better for standing poses)
            width, height = 1024, 1364
        elif body_composition == 'face':
            # Square for face close-ups
            width, height = 1024, 1024
        else:  # half body
            # Square or slightly portrait for half body
            width, height = 1024, 1024
        
        # Generate profile image with Danbooru tags
        profile_prompt = f"{composition_desc}, {outfit_desc}, smile, looking at viewer, beautiful eyes, soft lighting"
        
        # Use existing reference if available, otherwise this will be the first image (no reference)
        reference_img = reference_images.get(session_id)
        result = ComfyUIClient.generate_image(profile_prompt, image_type="CASUAL", width=width, height=height, character_description=character_desc, reference_image=reference_img)
        
        # Mark this prompt to be saved as reference image when complete
        if not reference_img:  # Only save as reference if we don't have one yet
            pending_reference_saves[result.get('prompt_id')] = session_id
        
        return jsonify({
            "status": "success",
            "prompt_id": result.get('prompt_id'),
            "message": f"Generating {girlfriend_name}'s profile picture..."
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/image-status/<prompt_id>', methods=['GET'])
def image_status(prompt_id):
    """Check status of image generation and get image URL if ready"""
    try:
        status = ComfyUIClient.get_image_status(prompt_id)
        
        if status['status'] == 'completed':
            # Get the image URL
            image_url = ComfyUIClient.get_image_url(
                status['filename'],
                status.get('subfolder', ''),
                status.get('type', 'output')
            )
            
            # Check if this image should be saved as a reference
            if prompt_id in pending_reference_saves:
                session_id = pending_reference_saves[prompt_id]
                # Store the filename with subfolder info for future generations
                # ComfyUI LoadImage needs just the filename for images in the output folder
                filename = status['filename']
                subfolder = status.get('subfolder', '')
                
                # For images in output folder, use filename as-is
                # For images in subfolders, include the subfolder path
                if subfolder:
                    reference_images[session_id] = f"{subfolder}/{filename}"
                else:
                    reference_images[session_id] = filename
                    
                # Remove from pending
                del pending_reference_saves[prompt_id]
                print(f"[ControlNet] Saved reference image for session {session_id}: {reference_images[session_id]}")
            
            return jsonify({
                'status': 'completed',
                'image_url': image_url,
                'filename': status['filename']
            })
        else:
            return jsonify(status)
            
    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500


@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """Generate an image based on description"""
    try:
        data = request.json
        prompt = data.get('prompt', '')
        
        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        # Enhance prompt for wholesome girlfriend avatar
        enhanced_prompt = f"beautiful anime girl portrait, {prompt}, warm smile, kind eyes, soft lighting, high quality, detailed"
        
        result = ComfyUIClient.generate_image(enhanced_prompt)
        
        return jsonify({
            "status": "success",
            "prompt_id": result.get('prompt_id'),
            "message": "Image generation started"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/unlock-intimacy', methods=['POST'])
def unlock_intimacy():
    """Unlock intimacy level with tokens"""
    try:
        data = request.json
        session_id = data.get('session_id')
        intimacy_type = data.get('intimacy_type')  # 'FLIRTY' or 'INTIMATE'
        
        if not session_id or not intimacy_type:
            return jsonify({"error": "Missing required parameters"}), 400
        
        if intimacy_type not in INTIMACY_UNLOCK_COSTS:
            return jsonify({"error": "Invalid intimacy type"}), 400
        
        # Check token balance
        current_tokens = intimacy_tokens.get(session_id, 0)
        cost = INTIMACY_UNLOCK_COSTS[intimacy_type]
        
        if current_tokens < cost:
            return jsonify({
                "error": f"Not enough tokens. Need {cost}, have {current_tokens}",
                "tokens_needed": cost - current_tokens
            }), 400
        
        # Check if already unlocked
        if session_id not in unlocked_intimacy:
            unlocked_intimacy[session_id] = set()
        
        if intimacy_type in unlocked_intimacy[session_id]:
            return jsonify({"error": f"{intimacy_type} already unlocked"}), 400
        
        # Unlock and deduct tokens
        intimacy_tokens[session_id] -= cost
        unlocked_intimacy[session_id].add(intimacy_type)
        
        # Auto-unlock lower levels
        if intimacy_type == 'INTIMATE':
            unlocked_intimacy[session_id].add('FLIRTY')
        
        return jsonify({
            "status": "success",
            "message": f"{intimacy_type} content unlocked!",
            "tokens_remaining": intimacy_tokens[session_id],
            "unlocked": list(unlocked_intimacy[session_id]),
            "max_intimacy": get_max_intimacy_level(session_id)
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear conversation history"""
    try:
        data = request.json
        session_id = data.get('session_id')
        language = data.get('language', 'en')
        
        if session_id and session_id in conversations:
            # Keep system prompt but clear conversation
            girlfriend_name = girlfriend_names.get(session_id, 'Luna')
            current_affection = affection_levels.get(session_id, 0)
            level_key, _ = get_affection_level_info(current_affection)
            conversations[session_id] = [
                {"role": "system", "content": get_girlfriend_prompt(girlfriend_name, level_key, current_affection, session_id, language)}
            ]
        
        return jsonify({"status": "success", "message": "Conversation cleared"})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def prime_ollama():
    """Prime Ollama by sending a test prompt to load the model and keep it loaded"""
    try:
        print("📡 Priming Ollama model...")
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": "Hi",
                "stream": False,
                "keep_alive": -1  # Keep model loaded indefinitely
            },
            timeout=30
        )
        if response.status_code == 200:
            print("✅ Ollama model loaded and kept in memory (keep_alive: indefinite)")
        else:
            print("⚠️ Ollama priming failed (service may still work)")
    except Exception as e:
        print(f"⚠️ Ollama priming error: {e} (service may still work)")


def wait_for_comfyui():
    """Wait for ComfyUI server to be running and accessible"""
    import time
    
    print("🎨 Waiting for ComfyUI server to start...")
    
    max_wait_time = 300  # 5 minutes
    check_interval = 5    # Check every 5 seconds
    elapsed_time = 0
    
    while elapsed_time < max_wait_time:
        try:
            # Check if ComfyUI is accessible
            response = requests.get(f"{COMFYUI_BASE_URL}/system_stats", timeout=10)
            if response.status_code == 200:
                print(f"✅ ComfyUI server is running (took {elapsed_time} seconds)")
                return True  # Server confirmed running
                
        except Exception as e:
            # ComfyUI not ready yet, continue waiting
            if elapsed_time == 0:
                print(f"   ⏳ ComfyUI not ready yet, waiting...")
            elif elapsed_time % 30 == 0:  # Print update every 30 seconds
                print(f"   ⏳ Still waiting... ({elapsed_time}s / {max_wait_time}s)")
        
        time.sleep(check_interval)
        elapsed_time += check_interval
    
    # Timeout reached
    print(f"⚠️ ComfyUI wait timeout after {max_wait_time} seconds (service may still work)")
    return False


def prime_comfyui():
    """Prime ComfyUI by loading checkpoint into VRAM"""
    
    # First, wait for ComfyUI to be confirmed running
    if not wait_for_comfyui():
        return  # Timeout reached, skip priming
    
    # Deep priming: Load checkpoint by generating a tiny test image
    # Set PRIME_COMFYUI_DEEP=true in .env to enable (adds ~10-30 seconds to startup)
    deep_prime = os.getenv('PRIME_COMFYUI_DEEP', 'false').lower() == 'true'
    if deep_prime:
        print("🔄 Loading checkpoint into VRAM (this may take 10-30 seconds)...")
        try:
            # Generate a tiny 64x64 test image to load the model into VRAM
            test_workflow = ComfyUIClient.generate_image(
                "test", 
                image_type="CASUAL", 
                width=64, 
                height=64
            )
            print("✅ Checkpoint loaded into VRAM - ready for fast generation!")
        except Exception as e:
            print(f"⚠️ Checkpoint loading failed: {e}")
    else:
        print("ℹ️  Deep priming disabled. Set PRIME_COMFYUI_DEEP=true in .env to preload checkpoint.")
        print("✅ ComfyUI ready (checkpoint will load on first image generation)")


if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("\n" + "="*50)
    print("🌸 SweetGF - Virtual Girlfriend Experience 🌸")
    print("="*50)
    print(f"\n✨ Server starting on http://localhost:{port}")
    print(f"📡 Ollama: {OLLAMA_BASE_URL}")
    print(f"🎨 ComfyUI: {COMFYUI_BASE_URL}")
    print(f"🎯 ControlNet: {CONTROLNET_MODEL} (strength: {CONTROLNET_STRENGTH})")
    print("\n" + "="*50 + "\n")
    
    # Prime both services
    print("🔥 Priming services...\n")
    prime_ollama()
    prime_comfyui()
    print("\n" + "="*50)
    print("✅ All systems ready!")
    print("="*50 + "\n")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
