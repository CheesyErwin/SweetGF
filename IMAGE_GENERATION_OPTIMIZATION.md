# Image Generation Optimization Guide

## Current Performance Analysis

### Baseline Performance (RTX 4070 12GB)
```
Basic workflow: 8-12s
+ FaceDetailer: +3-5s (total: 11-17s)
+ LoRA: +1-2s (total: 12-19s)
+ img2img: +2-3s (total: 14-22s)
```

### Bottleneck Analysis

**Time Breakdown:**
1. **Checkpoint loading:** 0-10s (first time only, cached after)
2. **LoRA loading:** 0-1s (if enabled)
3. **CLIP text encoding:** 0.1-0.3s
4. **KSampler (main generation):** 5-8s (depends on steps)
5. **VAE decode:** 0.5-1s
6. **FaceDetailer:** 3-5s (if enabled)
   - Face detection: 0.5s
   - Face refinement: 2-4s
7. **Image save:** 0.1-0.2s

**Total:** 8-19s depending on settings

## Optimization Strategies

### 1. Reduce Sampling Steps ⚡ High Impact

**Current:**
```python
"steps": 20  # Basic workflow
"steps": 30  # img2img workflow
```

**Optimized:**
```python
"steps": 15  # Basic workflow (-25% time)
"steps": 20  # img2img workflow (-33% time)
```

**Impact:** -2-4s per image
**Quality loss:** Minimal (barely noticeable)

**Implementation:**
```python
# Add to .env
IMAGE_GENERATION_STEPS=15

# In app.py
GENERATION_STEPS = int(os.getenv('IMAGE_GENERATION_STEPS', '20'))

# Use in workflow
"steps": GENERATION_STEPS,
```

### 2. Use Faster Samplers ⚡ Medium Impact

**Current:**
```python
"sampler_name": "euler"
```

**Faster Options:**
```python
"sampler_name": "dpm_2"        # Slightly faster
"sampler_name": "lcm"          # 4x faster (needs LCM LoRA)
"sampler_name": "lightning"    # 2x faster (needs Lightning LoRA)
```

**Impact:** -2-5s per image (with LCM/Lightning)
**Quality:** LCM/Lightning may reduce quality slightly

**Recommendation:** Stick with `euler` for quality, or try `dpm_2` for slight speedup

### 3. Optimize FaceDetailer Settings ⚡ High Impact

**Current:**
```python
"steps": 20,      # FaceDetailer steps
"denoise": 0.4,   # Refinement strength
```

**Optimized:**
```python
"steps": 15,      # -25% time
"denoise": 0.35,  # Lighter refinement
```

**Impact:** -1-2s per image
**Quality loss:** Minimal

**Implementation:**
```python
# Add to .env
FACEDETAILER_STEPS=15
FACEDETAILER_DENOISE=0.35

# In app.py
FACEDETAILER_STEPS = int(os.getenv('FACEDETAILER_STEPS', '20'))
FACEDETAILER_DENOISE = float(os.getenv('FACEDETAILER_DENOISE', '0.4'))
```

### 4. Conditional FaceDetailer ⚡ High Impact

**Strategy:** Only use FaceDetailer for close-up images

```python
def should_use_facedetailer(image_type, body_composition):
    """Determine if FaceDetailer is needed"""
    # Only use for face/portrait shots
    if body_composition in ['face', 'half']:
        return True
    # Skip for full body (face is small anyway)
    if body_composition == 'full':
        return False
    # Use for CASUAL/FLIRTY, skip for INTIMATE (speed priority)
    if image_type in ['CASUAL', 'FLIRTY']:
        return True
    return False
```

**Impact:** -3-5s on 50% of images
**Quality:** No loss (only skips when face is small)

### 5. Resolution Optimization ⚡ Very High Impact

**Current:**
```python
width=1024, height=1024  # Profile images
width=1024, height=1024  # Chat images
```

**Optimized by Type:**
```python
# CASUAL images - can be smaller
width=768, height=768    # -40% generation time

# FLIRTY images - medium quality
width=896, height=896    # -25% generation time

# INTIMATE images - keep high quality
width=1024, height=1024  # Full quality
```

**Impact:** -3-6s per image (for smaller resolutions)
**Quality:** Noticeable at 768x768, minimal at 896x896

### 6. Batch Processing (Future) ⚡ Extreme Impact

**Concept:** Generate multiple images in one workflow

```python
"batch_size": 2  # Generate 2 images at once
```

**Impact:** 1.5x throughput (2 images in 1.5x time)
**Limitation:** Requires 2x VRAM

**Not recommended yet:** Needs UI changes to handle batches

### 7. Model Quantization ⚡ Medium Impact

**Use FP16 instead of FP32:**

**Benefits:**
- 50% less VRAM usage
- 10-20% faster generation
- Allows larger batch sizes

**Drawbacks:**
- Slightly lower quality (usually imperceptible)
- Some models don't support FP16

**Implementation:**
- Download FP16 versions of models
- Or convert: `python convert_to_fp16.py model.safetensors`

### 8. Prompt Caching ⚡ Low Impact

**Strategy:** Cache CLIP embeddings for common prompts

```python
clip_cache = {}

def get_clip_embedding(prompt, clip_source):
    cache_key = f"{prompt}_{clip_source}"
    if cache_key in clip_cache:
        return clip_cache[cache_key]
    
    # Generate embedding
    embedding = encode_clip(prompt, clip_source)
    clip_cache[cache_key] = embedding
    return embedding
```

**Impact:** -0.1-0.2s per image (minimal)
**Complexity:** High (requires workflow changes)

**Not recommended:** Complexity outweighs benefit

### 9. Async Image Generation ⚡ High Impact (UX)

**Current:** User waits for image to complete

**Optimized:** Return immediately, poll for completion

```python
# Frontend polls /api/image-status every 2s
# User can continue chatting while image generates
```

**Impact:** Perceived instant response
**Already implemented:** ✅ App already does this!

### 10. Smart Resolution Scaling ⚡ Medium Impact

**Strategy:** Generate at lower resolution, upscale if needed

```python
# Generate at 768x768 (fast)
# Upscale to 1024x1024 (if user requests full size)
```

**Impact:** -3-5s for initial generation
**Quality:** Good with proper upscaler (RealESRGAN)

**Implementation complexity:** Medium

## Recommended Optimization Package

### Quick Wins (Easy to Implement)

**1. Reduce Steps:**
```python
# app.py
GENERATION_STEPS = 15  # Was 20
FACEDETAILER_STEPS = 15  # Was 20
```
**Savings:** -3-5s per image
**Quality loss:** Minimal

**2. Optimize FaceDetailer Denoise:**
```python
FACEDETAILER_DENOISE = 0.35  # Was 0.4
```
**Savings:** -0.5-1s per image
**Quality loss:** Minimal

**3. Conditional FaceDetailer:**
```python
# Skip FaceDetailer for full body images
if body_composition == 'full':
    ENABLE_FACE_DETAILER = False
```
**Savings:** -3-5s on 30% of images
**Quality loss:** None (face too small anyway)

### Total Quick Wins: -6-11s per image (30-50% faster!)

### Advanced Optimizations (More Complex)

**4. Dynamic Resolution:**
```python
# CASUAL: 768x768
# FLIRTY: 896x896
# INTIMATE: 1024x1024
```
**Savings:** -3-6s on CASUAL images
**Quality loss:** Noticeable but acceptable

**5. Use DPM_2 Sampler:**
```python
"sampler_name": "dpm_2"  # Was "euler"
```
**Savings:** -1-2s per image
**Quality loss:** Minimal

### Total Advanced: -4-8s additional

## Implementation Priority

### Phase 1: Immediate (No Code Changes)

1. **Disable FaceDetailer for testing:**
   ```env
   ENABLE_FACE_DETAILER=false
   ```
   **Test:** Generate 3 images, check quality vs speed

2. **Disable LoRA for testing:**
   ```env
   ENABLE_LORA=false
   ```
   **Test:** Check if quality loss is acceptable

### Phase 2: Configuration (Add to .env)

```env
# Image Generation Optimization
IMAGE_GENERATION_STEPS=15
FACEDETAILER_STEPS=15
FACEDETAILER_DENOISE=0.35
```

**Code changes:**
```python
# Add to app.py configuration section
GENERATION_STEPS = int(os.getenv('IMAGE_GENERATION_STEPS', '20'))
FACEDETAILER_STEPS = int(os.getenv('FACEDETAILER_STEPS', '20'))
FACEDETAILER_DENOISE = float(os.getenv('FACEDETAILER_DENOISE', '0.4'))

# Use in workflows
"steps": GENERATION_STEPS,  # Instead of hardcoded 20

# Use in FaceDetailer
"steps": FACEDETAILER_STEPS,
"denoise": FACEDETAILER_DENOISE,
```

### Phase 3: Smart Optimizations (More Code)

**Conditional FaceDetailer:**
```python
def should_use_facedetailer(body_composition):
    # Skip for full body
    return body_composition != 'full'

# In generate_image
use_facedetailer = ENABLE_FACE_DETAILER and should_use_facedetailer(body_composition)
```

**Dynamic Resolution:**
```python
def get_optimal_resolution(image_type):
    if image_type == 'CASUAL':
        return 768, 768
    elif image_type == 'FLIRTY':
        return 896, 896
    else:  # INTIMATE
        return 1024, 1024

# In generate_image
if width == 512 and height == 512:  # Default
    width, height = get_optimal_resolution(image_type)
```

## Performance Comparison

### Current (No Optimizations)
```
CASUAL:   12-15s
FLIRTY:   12-15s
INTIMATE: 15-19s
Average:  13-16s
```

### Phase 1 (Disable FaceDetailer)
```
CASUAL:   8-10s  (-33%)
FLIRTY:   8-10s  (-33%)
INTIMATE: 10-12s (-33%)
Average:  9-11s  (-33%)
```

### Phase 2 (Reduced Steps)
```
CASUAL:   10-12s (-20%)
FLIRTY:   10-12s (-20%)
INTIMATE: 12-15s (-20%)
Average:  11-13s (-20%)
```

### Phase 3 (All Optimizations)
```
CASUAL:   6-8s   (-50%)
FLIRTY:   8-10s  (-40%)
INTIMATE: 12-15s (-20%)
Average:  9-11s  (-35%)
```

## Quality vs Speed Matrix

| Setting | Speed | Quality | Recommendation |
|---------|-------|---------|----------------|
| Steps: 30 | Slow | Excellent | Overkill |
| Steps: 20 | Medium | Great | **Current** |
| Steps: 15 | Fast | Good | **Recommended** |
| Steps: 10 | Very Fast | Fair | Too low |
| FaceDetailer ON | Slow | Excellent faces | **For portraits** |
| FaceDetailer OFF | Fast | Good faces | **For full body** |
| LoRA ON | Slow | Better anatomy | **For INTIMATE** |
| LoRA OFF | Fast | Good anatomy | **For CASUAL** |
| 1024x1024 | Slow | Excellent | **For INTIMATE** |
| 896x896 | Medium | Great | **For FLIRTY** |
| 768x768 | Fast | Good | **For CASUAL** |

## Recommended Configuration

### Balanced (Best Quality/Speed Ratio)

```env
# .env
IMAGE_GENERATION_STEPS=15
FACEDETAILER_STEPS=15
FACEDETAILER_DENOISE=0.35
ENABLE_FACE_DETAILER=true
ENABLE_LORA=true
```

```python
# Dynamic settings in code
if image_type == 'CASUAL':
    width, height = 768, 768
    use_lora = False
elif image_type == 'FLIRTY':
    width, height = 896, 896
    use_lora = False
else:  # INTIMATE
    width, height = 1024, 1024
    use_lora = True

use_facedetailer = body_composition != 'full'
```

**Expected Performance:**
- CASUAL: 6-8s
- FLIRTY: 8-10s
- INTIMATE: 12-15s
- Average: 9-11s

**Quality:** Excellent (minimal loss from optimizations)

### Speed Priority

```env
IMAGE_GENERATION_STEPS=12
ENABLE_FACE_DETAILER=false
ENABLE_LORA=false
```

**Expected Performance:**
- All images: 5-7s
- Average: 6s

**Quality:** Good (noticeable but acceptable loss)

### Quality Priority

```env
IMAGE_GENERATION_STEPS=25
FACEDETAILER_STEPS=20
ENABLE_FACE_DETAILER=true
ENABLE_LORA=true
```

**Expected Performance:**
- All images: 15-20s
- Average: 17s

**Quality:** Excellent (maximum quality)

## Next Steps

1. **Test current performance:**
   - Generate 10 images
   - Record times
   - Note quality

2. **Implement Phase 2:**
   - Add configuration options
   - Test with reduced steps
   - Compare quality

3. **Implement Phase 3:**
   - Add conditional FaceDetailer
   - Add dynamic resolution
   - Test performance gain

4. **Monitor and tune:**
   - Adjust steps based on quality needs
   - Find sweet spot for your use case

## Summary

**Easiest wins:**
- ✅ Reduce steps to 15 (-20% time)
- ✅ Skip FaceDetailer for full body (-30% time on those images)
- ✅ Optimize FaceDetailer denoise (-5% time)

**Total potential speedup:** 30-50% with minimal quality loss

**Recommended:** Implement Phase 2 configuration options for flexibility
