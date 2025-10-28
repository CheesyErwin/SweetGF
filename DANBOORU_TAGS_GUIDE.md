# Danbooru Tags Guide for Image Generation

## 🎨 What Are Danbooru Tags?

Danbooru is an anime image board that uses a comprehensive tagging system. Anime-focused AI models (like the one you're using) are trained on datasets tagged with Danbooru conventions, making them **highly responsive** to this format.

**Benefits:**
- ✅ More accurate image generation
- ✅ Better control over explicit content
- ✅ Consistent character features
- ✅ Precise pose/clothing control

---

## 📝 Tag Format

**Structure:** Comma-separated tags, underscores for multi-word concepts

```
masterpiece, best quality, 1girl, long_hair, blue_eyes, school_uniform, smile, looking_at_viewer
```

**NOT like this:**
```
A beautiful anime girl with long hair wearing a school uniform
```

---

## 🏷️ Tag Categories

### **1. Quality Tags** (Always include these first)

```
masterpiece, best quality, high resolution, detailed
```

**Negative quality:**
```
low quality, worst quality, blurry, jpeg artifacts
```

### **2. Character Count**

```
1girl          # Single female character
1boy           # Single male character  
2girls         # Two girls
1girl, 1boy    # One of each
```

### **3. Hair Tags**

**Length:**
```
long hair, short hair, medium hair, very long hair
```

**Color:**
```
brown hair, black hair, blonde hair, red hair, blue hair, white hair, pink hair
```

**Style:**
```
ponytail, twin tails, braided hair, straight hair, wavy hair, messy hair
```

### **4. Eye Tags**

**Color:**
```
amber eyes, blue eyes, green eyes, red eyes, purple eyes, heterochromia
```

**Style:**
```
looking at viewer, closed eyes, half-closed eyes, glowing eyes
```

### **5. Body/Appearance**

**Build:**
```
slender, slim body, curvy, petite, tall
```

**Breasts:**
```
flat chest, small breasts, medium breasts, large breasts, huge breasts
```

**Skin:**
```
pale skin, tan, dark skin
```

### **6. Clothing Tags**

**Common outfits:**
```
school uniform, dress, casual clothes, kimono, swimsuit, bikini
t-shirt, jeans, skirt, shorts, sweater, coat
```

**Clothing state:**
```
clothed, partially clothed, topless, bottomless, naked, nude
```

### **7. Pose/Action Tags**

**Standing:**
```
standing, arms at sides, hand on hip, one hand up
```

**Sitting:**
```
sitting, sitting on chair, sitting on bed, crossed legs
```

**Lying:**
```
lying, on back, on stomach, on side
```

### **8. Expression Tags**

```
smile, grin, blush, embarrassed, angry, sad, surprised, seductive
open mouth, closed mouth, tongue out
```

### **9. Camera/Framing**

```
portrait, close-up, upper body, full body, from above, from below
looking at viewer, looking away, looking back
```

---

## 🔞 Explicit Danbooru Tags

### **NSFW Base Tags**

```
nsfw, explicit, uncensored
```

### **Nudity Tags**

```
nude, naked, completely nude
topless, bottomless
nipples, breasts, pussy, ass
```

### **Explicit Anatomy**

**Breasts:**
```
nipples, areolae, large nipples, erect nipples
breast grab, breast squeeze, bouncing breasts
```

**Genitals:**
```
pussy, clitoris, pussy juice, wet pussy
spread pussy, fingering, masturbation
```

**Poses/Actions:**
```
legs spread, open legs, M-legs, spread legs
on back, lying, arched back
kneeling, all fours, ass up
```

### **Sexual Acts**

```
sex, vaginal, penetration, insertion
fellatio, cunnilingus, fingering
masturbation, touching self, self fondle
orgasm, ahegao, pleasure, aroused
```

### **Fluids**

```
pussy juice, cum, sweat, saliva
wet, dripping, leaking
```

### **Clothing in NSFW**

```
clothes lift, skirt lift, dress lift
clothing aside, panties aside
torn clothes, ripped clothes
see-through, transparent
```

---

## 🎯 Example Prompts

### **CASUAL (SFW)**

```
masterpiece, best quality, 1girl, long brown hair, amber eyes, 
upper body, casual clothes, t-shirt, jeans, smile, looking at viewer, 
soft lighting, detailed, high resolution
```

### **FLIRTY (Suggestive)**

```
masterpiece, best quality, 1girl, long brown hair, amber eyes,
upper body, revealing clothes, cleavage, seductive, sexy pose,
alluring expression, blush, soft lighting, detailed, high resolution
```

### **INTIMATE (Explicit)**

```
masterpiece, best quality, 1girl, long brown hair, amber eyes,
nsfw, nude, naked, completely nude, pussy, breasts, nipples,
explicit, uncensored, legs spread, pussy juice, aroused, 
on back, looking at viewer, seductive expression, erotic, sexual,
detailed, high resolution
```

---

## ⚙️ Current Implementation

### **Character Description**

```python
'1girl, long brown hair, amber eyes, slender body, 
medium breasts, beautiful face, detailed face, anime style'
```

### **CASUAL Images**

```
masterpiece, best quality, [character], [prompt], 
casual clothes, natural lighting, detailed, high resolution
```

### **FLIRTY Images**

```
masterpiece, best quality, [character], [prompt], 
suggestive, seductive, revealing clothes, sexy pose, 
alluring expression, soft lighting, detailed, high resolution
```

### **INTIMATE Images**

```
masterpiece, best quality, [character], [prompt],
nsfw, nude, naked, completely nude, pussy, breasts, nipples,
explicit, uncensored, legs spread, pussy juice, aroused, 
erotic, sexual, sensual pose, seductive expression, 
intimate, detailed, high resolution
```

---

## 🔧 Customization

### **Change Character Appearance**

Edit `app.py` line 300:

```python
'full_description': '1girl, long silver hair, red eyes, pale skin, 
large breasts, beautiful face, detailed face, anime style'
```

### **Add More Explicit Tags**

Edit `app.py` line 326 for INTIMATE images:

```python
explicit_tags = "nsfw, nude, naked, pussy, breasts, nipples, 
explicit, uncensored, legs spread, fingering, masturbation, 
pussy juice, orgasm, aroused, ahegao, erotic, sexual"
```

### **Adjust Outfit Tags**

Edit outfit_descriptions in `app.py` around line 668:

```python
'casual': 'casual clothes, t-shirt, jeans, sneakers',
'bikini': 'swimsuit, bikini, string bikini, beach',
```

---

## 📊 Tag Strength

Tags earlier in the prompt have **more weight**. Order matters!

**Good order:**
```
masterpiece, best quality, 1girl, long brown hair, amber eyes, 
nude, breasts, nipples, pussy, legs spread
```

**Less effective:**
```
legs spread, pussy, nipples, breasts, nude, 
long brown hair, amber eyes, 1girl, masterpiece
```

---

## 🚫 Negative Prompt

Current negative tags (automatically applied):

```
low quality, worst quality, blurry, distorted, deformed, 
bad anatomy, bad hands, bad fingers, mutated hands, 
extra digits, fewer digits, jpeg artifacts, watermark, 
signature, text
```

**Add if needed:**
- `censored` - Removes mosaic/censorship
- `clothed` - For nude images
- `pubic hair` - If you don't want it

---

## 💡 Tips

1. **Be specific:** "long brown hair" > "hair"
2. **Use multiple tags:** "nude, naked, completely nude" reinforces
3. **Consistent format:** Stick to Danbooru conventions
4. **Quality first:** Always start with quality tags
5. **Character count:** Always include "1girl"
6. **For explicit:** Don't be shy, use direct anatomical terms

---

## 🎨 Result Quality

**Before Danbooru tags:**
- Vague prompts → inconsistent results
- "Natural language" → model confusion
- Hit or miss explicit content

**After Danbooru tags:**
- ✅ Precise control
- ✅ Better anatomy
- ✅ Consistent style
- ✅ Reliable explicit content
- ✅ Higher quality outputs

---

## 📚 Resources

- **Danbooru Wiki:** https://danbooru.donmai.us/wiki_pages/tag_groups
- **Tag Search:** https://danbooru.donmai.us/tags
- **Popular Tags:** https://danbooru.donmai.us/tags?sort=count

Your girlfriend's images will now be much more consistent and responsive to explicit requests! 🎨🔥
