# VRAM Optimization Guide

## Problem: Models Reloading Every Generation

### Symptoms:
- First image: 8-10s
- Second image: 8-10s (should be faster!)
- Third image: 8-10s (still slow!)
- Console shows: "Loading checkpoint..." every time

### Root Cause:

**ComfyUI VRAM Management Modes:**

ComfyUI has different modes for managing GPU memory:

1. **Auto (Default)** - Unloads models when not in use
2. **GPU-Only** - Keeps models in VRAM permanently
3. **High VRAM** - Aggressive caching
4. **Normal VRAM** - Balanced approach
5. **Low VRAM** - Minimal VRAM usage
6. **No VRAM** - CPU only

**The Issue:**
- Default mode unloads models after each generation
- Next generation reloads from disk (slow!)
- With `--gpu-only`, models stay in VRAM (fast!)

## Solution: Use --gpu-only Flag

### What It Does:

**Without --gpu-only (Default):**
```
Generation 1:
- Load checkpoint (5-8s)
- Generate image (3-5s)
- Unload checkpoint
Total: 8-13s

Generation 2:
- Load checkpoint again (5-8s) ← Slow!
- Generate image (3-5s)
- Unload checkpoint
Total: 8-13s
```

**With --gpu-only:**
```
Generation 1:
- Load checkpoint (5-8s)
- Generate image (3-5s)
- Keep in VRAM ✓
Total: 8-13s

Generation 2:
- Checkpoint already loaded ✓
- Generate image (3-5s)
Total: 3-5s (60% faster!)

Generation 3+:
- Still loaded ✓
- Generate image (3-5s)
Total: 3-5s (consistently fast!)
```

### Implementation:

**Updated `start_comfyui.bat`:**
```batch
# Portable version
call run_nvidia_gpu.bat --gpu-only

# Standard installation
python main.py --gpu-only
```

**Effect:**
- Checkpoint stays in VRAM
- LoRA stays in VRAM
- VAE stays in VRAM
- Upscale models stay in VRAM

## VRAM Management Options

### Option 1: --gpu-only (Recommended)

**Command:**
```bash
python main.py --gpu-only
```

**Behavior:**
- Keeps all models in VRAM
- Never unloads
- Fastest generation

**VRAM Usage:**
- Checkpoint: ~6-8GB
- LoRA: ~100MB
- VAE: ~300MB
- Total: ~7-9GB

**Best for:**
- 12GB+ VRAM
- Fastest performance
- Consistent speed

**Pros:**
- ✅ Fastest generation (3-5s after first)
- ✅ No model reloading
- ✅ Consistent performance

**Cons:**
- ❌ Uses VRAM constantly
- ❌ May compete with Ollama

---

### Option 2: --highvram

**Command:**
```bash
python main.py --highvram
```

**Behavior:**
- Aggressive VRAM caching
- Keeps most models loaded
- Unloads only when necessary

**VRAM Usage:**
- Similar to --gpu-only
- Slightly more flexible

**Best for:**
- 16GB+ VRAM
- Multiple models
- Heavy workflows

---

### Option 3: --normalvram (Default)

**Command:**
```bash
python main.py --normalvram
# or just
python main.py
```

**Behavior:**
- Balanced approach
- Unloads models when idle
- Reloads when needed

**VRAM Usage:**
- Dynamic (2-10GB)
- Frees when idle

**Best for:**
- 8-12GB VRAM
- Shared GPU usage
- Occasional generation

**Pros:**
- ✅ Frees VRAM when idle
- ✅ Works with Ollama

**Cons:**
- ❌ Reloads models (5-8s overhead)
- ❌ Inconsistent speed

---

### Option 4: --lowvram

**Command:**
```bash
python main.py --lowvram
```

**Behavior:**
- Minimal VRAM usage
- Loads/unloads aggressively
- Slower but works on low VRAM

**VRAM Usage:**
- 4-6GB peak
- Minimal idle usage

**Best for:**
- 6-8GB VRAM
- Old GPUs
- VRAM-constrained systems

**Cons:**
- ❌ Very slow (10-15s per image)
- ❌ Constant loading/unloading

---

### Option 5: --cpu

**Command:**
```bash
python main.py --cpu
```

**Behavior:**
- CPU-only generation
- No GPU usage

**Best for:**
- No GPU
- Testing
- Debugging

**Cons:**
- ❌ Extremely slow (2-5 minutes per image)

## Performance Comparison

### First Generation (Cold Start)

| Mode | Time | VRAM |
|------|------|------|
| --gpu-only | 8-10s | 8GB |
| --highvram | 8-10s | 8GB |
| --normalvram | 8-10s | 8GB |
| --lowvram | 12-15s | 6GB |
| --cpu | 120-300s | 0GB |

### Subsequent Generations (Warm)

| Mode | Time | VRAM |
|------|------|------|
| --gpu-only | 3-5s ✅ | 8GB |
| --highvram | 3-5s ✅ | 8GB |
| --normalvram | 8-10s ❌ | 2-8GB |
| --lowvram | 12-15s ❌ | 6GB |
| --cpu | 120-300s ❌ | 0GB |

**Winner:** `--gpu-only` for consistent fast performance!

## Recommended Settings

### For 12GB VRAM (RTX 3060/4070)

**ComfyUI:**
```bash
python main.py --gpu-only
```

**Ollama:**
```bash
# Run on CPU to free GPU for ComfyUI
set OLLAMA_NUM_GPU=0
ollama serve
```

**Result:**
- ComfyUI: Full GPU (fast images)
- Ollama: CPU (acceptable text speed)
- No VRAM conflicts

---

### For 16GB VRAM (RTX 4080)

**ComfyUI:**
```bash
python main.py --gpu-only
```

**Ollama:**
```bash
# Both can share GPU
ollama serve
```

**With Resource Lock:**
```env
ENABLE_RESOURCE_LOCK=true
```

**Result:**
- Both use GPU
- Sequential processing prevents conflicts
- Fast generation for both

---

### For 24GB VRAM (RTX 4090)

**ComfyUI:**
```bash
python main.py --gpu-only
```

**Ollama:**
```bash
ollama serve
```

**No Resource Lock:**
```env
ENABLE_RESOURCE_LOCK=false
```

**Result:**
- Both run simultaneously
- No conflicts
- Maximum speed

---

### For 8GB VRAM (RTX 3060 8GB)

**ComfyUI:**
```bash
python main.py --normalvram
```

**Ollama:**
```bash
# CPU only
set OLLAMA_NUM_GPU=0
ollama serve
```

**Optimizations:**
```env
ENABLE_FACE_DETAILER=false
ENABLE_UPSCALE=false
IMAGE_GENERATION_STEPS=12
```

**Result:**
- Slower but works
- No OOM errors
- Acceptable performance

## Checking Current Mode

### In ComfyUI Console:

**Look for:**
```
Starting server
To see the GUI go to: http://127.0.0.1:8188
VRAM: gpu-only
```

**Or:**
```
VRAM: normal
```

### Test Performance:

**Generate 3 images in a row:**
```
Image 1: 8-10s (loading)
Image 2: 3-5s (if --gpu-only) or 8-10s (if normal)
Image 3: 3-5s (if --gpu-only) or 8-10s (if normal)
```

**If Image 2 and 3 are slow, you're NOT using --gpu-only!**

## Troubleshooting

### Issue: Models still reloading

**Check:**
1. ComfyUI started with `--gpu-only` flag?
2. Console shows "VRAM: gpu-only"?
3. Using consistent checkpoint name?

**Solution:**
```bash
# Stop ComfyUI
# Restart with flag
python main.py --gpu-only
```

---

### Issue: Out of memory errors

**Symptoms:**
```
CUDA out of memory
RuntimeError: CUDA error
```

**Solution 1: Use lower VRAM mode**
```bash
python main.py --normalvram
```

**Solution 2: Run Ollama on CPU**
```bash
set OLLAMA_NUM_GPU=0
ollama serve
```

**Solution 3: Enable resource lock**
```env
ENABLE_RESOURCE_LOCK=true
```

---

### Issue: First image fast, second slow

**This means:**
- Models loaded on first gen
- Unloaded after completion
- Reloading on second gen

**Fix:**
```bash
# Add --gpu-only flag
python main.py --gpu-only
```

---

### Issue: Competing with Ollama

**Symptoms:**
- Both services slow
- VRAM errors
- Inconsistent performance

**Solution 1: Sequential processing**
```env
ENABLE_RESOURCE_LOCK=true
```

**Solution 2: Ollama on CPU**
```bash
set OLLAMA_NUM_GPU=0
ollama serve
```

**Solution 3: Smart keep-alive**
```env
OLLAMA_KEEP_ALIVE=5m
```

## Advanced: Custom VRAM Settings

### Hybrid Approach

**ComfyUI with --gpu-only:**
```bash
python main.py --gpu-only
```

**Ollama with smart unload:**
```env
OLLAMA_KEEP_ALIVE=5m
```

**Result:**
- ComfyUI: Always ready (3-5s)
- Ollama: Unloads after 5min idle
- Best of both worlds

### Memory Monitoring

**Check VRAM usage:**
```bash
nvidia-smi
```

**Expected with --gpu-only:**
```
ComfyUI idle: 7-9GB
ComfyUI generating: 10-12GB
Ollama loaded: +6-8GB
Total: 13-20GB
```

**If total > your VRAM:**
- Use --normalvram
- Or run Ollama on CPU

## Summary

### The Fix:

**Add `--gpu-only` flag to ComfyUI startup:**

```batch
# start_comfyui.bat
call run_nvidia_gpu.bat --gpu-only
```

**Effect:**
- First generation: 8-10s (loading)
- All subsequent: 3-5s (cached!)
- 60% faster after first image

### Verification:

**Test sequence:**
1. Start ComfyUI with `--gpu-only`
2. Generate first image (8-10s)
3. Generate second image (should be 3-5s!)
4. If still 8-10s, flag not applied

### Best Practices:

✅ Use `--gpu-only` for consistent speed  
✅ Run Ollama on CPU if VRAM limited  
✅ Enable resource lock if both on GPU  
✅ Monitor VRAM with `nvidia-smi`  
✅ Use smart keep-alive for Ollama  

**Your images will now generate 60% faster after the first one!** ⚡✨
