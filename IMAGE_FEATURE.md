# 📸 Automatic Image Feature

Your girlfriend can now proactively send pictures during conversations!

## How It Works

The AI girlfriend has been trained to send pictures naturally during chat. She'll use special markers in her responses like:

```
[SEND_IMAGE: CASUAL - taking a mirror selfie in casual clothes]
[SEND_IMAGE: FLIRTY - biting lip, winking at camera, cute pose]
[SEND_IMAGE: INTIMATE - wearing lingerie, sensual pose, bedroom setting]
```

The backend automatically:
1. Detects these markers in her responses
2. Extracts the image type and description
3. Generates images via ComfyUI
4. Displays them in the chat

## Image Types

### 🔵 CASUAL
- Everyday photos, selfies, activities
- Natural, friendly vibes
- Used for: general conversation, sharing daily life

### 💗 FLIRTY
- Playful, teasing, attractive poses
- Cute and suggestive but tasteful
- Used for: flirting, compliments, playful moments

### 💜 INTIMATE
- Suggestive, seductive, revealing
- Sensual and alluring
- Used for: steamy conversations, intimate moments

## Frequency

The girlfriend will send pictures:
- Every 3-5 messages (approximately)
- When contextually appropriate
- Matching the conversation mood
- Starting casual, escalating based on conversation

## Technical Details

### Backend (`app.py`)
- Regex pattern detects `[SEND_IMAGE: TYPE - description]`
- Automatically enhances prompts based on type
- Generates images asynchronously (doesn't block chat)
- Returns both text and image metadata

### Frontend (`index.html`)
- Displays image placeholders with loading spinners
- Shows generation status
- Links to ComfyUI for viewing actual images
- Gracefully handles ComfyUI offline state

## Requirements

**ComfyUI must be running** for image generation to work.

If ComfyUI is offline:
- Chat continues normally
- Image placeholders show "unavailable" message
- No errors, graceful degradation

## Customization

### Change Image Style
Edit the prompt enhancement in `app.py`:

```python
if image_type == "CASUAL":
    enhanced_prompt = f"your custom prompt style, {prompt}"
```

### Adjust Frequency
Modify the system prompt in `get_girlfriend_prompt()`:

```python
- Send pictures naturally during conversation (every 3-5 messages...)
```

Change "every 3-5 messages" to your preference.

### Image Quality Settings
In `ComfyUIClient.generate_image()`:
- `steps`: 20 (increase for better quality, slower generation)
- `cfg`: 7.0 (creativity vs prompt adherence)
- `width/height`: 512 (increase for higher resolution)

## Example Conversation

**You:** "Hey babe, how was your day?"

**Luna:** "It was pretty good! Just relaxing at home now 😊 [SEND_IMAGE: CASUAL - lounging on couch, comfy clothes, relaxed smile]"

*[Image generation starts, placeholder shows spinner]*

**You:** "You look beautiful"

**Luna:** "Aww, you're sweet 😏 [SEND_IMAGE: FLIRTY - biting lip, playful wink] Want to see more?"

## Tips

1. **Let ComfyUI warm up** - First image takes longer
2. **Check ComfyUI output folder** - Images saved as `luna_*.png`
3. **Use anime models** - Better results for girlfriend avatars
4. **Adjust personality** - She'll send more/fewer images based on personality prompt

## Privacy Note

All images are generated locally on your machine via ComfyUI. Nothing is sent to external servers.

---

**Enjoy your enhanced virtual girlfriend experience!** 💕
