# System Requirements & Performance Guide

## Minimum Requirements

### Hardware

**GPU (Critical):**
- **Minimum:** NVIDIA RTX 3060 12GB VRAM
- **Recommended:** NVIDIA RTX 4070 12GB+ VRAM
- **Optimal:** NVIDIA RTX 4090 24GB VRAM

**RAM:**
- **Minimum:** 16GB
- **Recommended:** 32GB
- **Optimal:** 64GB (for multiple concurrent sessions)

**Storage:**
- **Minimum:** 50GB free space (for models)
- **Recommended:** 100GB+ SSD
- Models: ~20-30GB
- Generated images: Grows over time

**CPU:**
- **Minimum:** 4-core processor
- **Recommended:** 8-core processor (for Ollama)

### Software

**Operating System:**
- Windows 10/11 (64-bit)
- Linux (Ubuntu 20.04+)
- macOS (limited GPU support)

**Python:**
- Python 3.10 or 3.11
- NOT compatible with Python 3.12+ yet

**CUDA:**
- CUDA 11.8 or 12.1
- cuDNN 8.x

## Performance Benchmarks

### Image Generation Times

**With Optimizations (keep_alive, VRAM management):**

| GPU | Resolution | FaceDetailer OFF | FaceDetailer ON |
|-----|-----------|------------------|-----------------|
| RTX 3060 12GB | 1024x1024 | 8-12s | 12-18s |
| RTX 4070 12GB | 1024x1024 | 5-8s | 8-12s |
| RTX 4090 24GB | 1024x1024 | 3-5s | 5-8s |

**Without Optimizations:**
- First generation: +10-30s (checkpoint loading)
- Each generation: +5-10s (model reload)

### Memory Usage

**Per Session:**
- Conversation history: ~1-5MB (with trimming)
- Character data: ~1KB
- Reference images: ~2-5MB

**Total Application:**
- Flask app: ~200-500MB
- Ollama (7B model): ~8-12GB RAM
- ComfyUI: ~4-8GB RAM
- GPU VRAM: ~10-12GB (checkpoint + LoRA + FaceDetailer)

## Performance Issues & Solutions

### Issue 1: Progressive Slowdown (Your Issue)

**Symptoms:**
- First image: 10-15s
- Second image: 20-25s
- Third image: 30-40s
- Eventually: 60s+

**Causes:**
1. **Conversation history growing** ✅ FIXED
   - Each message adds to context
   - Ollama processes entire history
   - Solution: Trim to last 20 messages

2. **ComfyUI queue buildup**
   - Multiple prompts queued
   - Solution: Wait for completion before next

3. **VRAM fragmentation**
   - Models loading/unloading
   - Solution: `keep_alive=-1` in Ollama

4. **Memory leak in sessions**
   - Old sessions not cleaned up
   - Solution: MAX_SESSIONS limit

**Fixes Applied:**
```python
# Conversation trimming
MAX_CONVERSATION_HISTORY = 20  # Keep last 10 exchanges

# Session cleanup
MAX_SESSIONS = 100  # Remove oldest when exceeded

# Auto-cleanup after each message
trim_conversation_history(session_id)
cleanup_old_sessions()
```

### Issue 2: First Generation Slow

**Solution:**
```env
PRIME_COMFYUI_DEEP=true
```
- Loads checkpoint into VRAM on startup
- Adds 10-30s to startup time
- Makes first generation fast

### Issue 3: Out of Memory (OOM)

**GPU OOM:**
```
RuntimeError: CUDA out of memory
```

**Solutions:**
1. Reduce image resolution:
   ```python
   width=768, height=768  # Instead of 1024x1024
   ```

2. Disable FaceDetailer:
   ```env
   ENABLE_FACE_DETAILER=false
   ```

3. Disable LoRA:
   ```env
   ENABLE_LORA=false
   ```

4. Use lower precision:
   - Use FP16 models instead of FP32
   - Enable `--lowvram` in ComfyUI

**RAM OOM:**
```
MemoryError: Unable to allocate array
```

**Solutions:**
1. Reduce MAX_CONVERSATION_HISTORY:
   ```python
   MAX_CONVERSATION_HISTORY = 10  # Instead of 20
   ```

2. Reduce MAX_SESSIONS:
   ```python
   MAX_SESSIONS = 50  # Instead of 100
   ```

3. Use smaller Ollama model:
   ```env
   OLLAMA_MODEL=llama2:7b  # Instead of 13b or 70b
   ```

### Issue 4: Slow Text Generation

**Ollama taking 10-30s per response:**

**Solutions:**
1. Use smaller model:
   - 7B models: Fast (5-10s)
   - 13B models: Medium (10-20s)
   - 70B models: Slow (30-60s)

2. Enable GPU acceleration:
   ```bash
   # Check Ollama is using GPU
   ollama ps
   # Should show GPU usage
   ```

3. Increase context window:
   ```python
   "options": {
       "num_ctx": 4096  # Increase if needed
   }
   ```

## Optimization Checklist

### ✅ Must-Have Optimizations

1. **Enable keep_alive:**
   - Ollama: `keep_alive: -1`
   - Prevents model unloading

2. **Enable conversation trimming:**
   - `MAX_CONVERSATION_HISTORY = 20`
   - Prevents memory growth

3. **Enable session cleanup:**
   - `MAX_SESSIONS = 100`
   - Prevents memory leaks

4. **Use consistent checkpoint:**
   - Don't switch models mid-session
   - Avoids reload delays

### ⚡ Performance Boosters

1. **Deep priming:**
   ```env
   PRIME_COMFYUI_DEEP=true
   ```

2. **VRAM management:**
   ```bash
   # ComfyUI startup
   python main.py --highvram
   # or
   python main.py --normalvram
   ```

3. **Disable unused features:**
   ```env
   ENABLE_FACE_DETAILER=false  # -3-5s per image
   ENABLE_LORA=false           # -1-2s per image
   ```

### 🎯 Quality vs Speed Trade-offs

**Maximum Quality (Slow):**
```env
ENABLE_FACE_DETAILER=true
ENABLE_LORA=true
# Resolution: 1024x1024
# Steps: 30
# Time: 15-25s per image
```

**Balanced (Recommended):**
```env
ENABLE_FACE_DETAILER=true
ENABLE_LORA=true
# Resolution: 1024x1024
# Steps: 20
# Time: 8-15s per image
```

**Maximum Speed (Fast):**
```env
ENABLE_FACE_DETAILER=false
ENABLE_LORA=false
# Resolution: 768x768
# Steps: 15
# Time: 5-8s per image
```

## Monitoring Performance

### Check Memory Usage

**Windows:**
```powershell
# GPU VRAM
nvidia-smi

# RAM
tasklist /FI "IMAGENAME eq python.exe"
```

**Linux:**
```bash
# GPU VRAM
nvidia-smi

# RAM
ps aux | grep python
```

### Check Generation Times

Look for these in ComfyUI console:
```
Prompt executed in 16.97 seconds  ← Good
Prompt executed in 32.78 seconds  ← Slowdown detected!
```

If times keep increasing:
1. Restart Flask app (clears conversation history)
2. Restart ComfyUI (clears VRAM fragmentation)
3. Check `MAX_CONVERSATION_HISTORY` setting

### Monitor Conversation Size

The app will log:
```
[Memory] Trimmed conversation history for session abc123 to 20 messages
[Memory] Cleaned up old session: xyz789
```

If you don't see these logs and generation is slow:
- Conversation history is growing
- Restart the app

## Recommended Configurations

### Budget Setup (RTX 3060 12GB)

```env
ENABLE_FACE_DETAILER=false
ENABLE_LORA=false
PRIME_COMFYUI_DEEP=true
```

```python
MAX_CONVERSATION_HISTORY = 10
MAX_SESSIONS = 50
```

**Expected Performance:**
- Image generation: 8-12s
- Text generation: 5-10s
- Concurrent users: 1-2

### Mid-Range Setup (RTX 4070 12GB)

```env
ENABLE_FACE_DETAILER=true
ENABLE_LORA=true
PRIME_COMFYUI_DEEP=true
```

```python
MAX_CONVERSATION_HISTORY = 20
MAX_SESSIONS = 100
```

**Expected Performance:**
- Image generation: 8-12s
- Text generation: 5-10s
- Concurrent users: 3-5

### High-End Setup (RTX 4090 24GB)

```env
ENABLE_FACE_DETAILER=true
ENABLE_LORA=true
PRIME_COMFYUI_DEEP=true
```

```python
MAX_CONVERSATION_HISTORY = 30
MAX_SESSIONS = 200
```

**Expected Performance:**
- Image generation: 5-8s
- Text generation: 3-5s
- Concurrent users: 10+

## Troubleshooting Slowdowns

### Step 1: Check Current Performance

Generate 3 images in a row. Check times:
- Image 1: __s
- Image 2: __s
- Image 3: __s

If times increase by >50%: Memory issue

### Step 2: Check Conversation Size

Look for trim logs:
```
[Memory] Trimmed conversation history...
```

If missing: Update to latest code

### Step 3: Restart Services

```bash
# Restart Flask
Ctrl+C
python app.py

# Restart ComfyUI
Ctrl+C
run_nvidia_gpu.bat
```

### Step 4: Check VRAM

```bash
nvidia-smi
```

If VRAM usage is 100%: Reduce quality settings

### Step 5: Reduce Settings

Try in order:
1. Disable FaceDetailer
2. Disable LoRA
3. Reduce resolution to 768x768
4. Reduce MAX_CONVERSATION_HISTORY to 10

## Summary

**Your Issue (Progressive Slowdown):**
- ✅ **FIXED:** Added conversation history trimming
- ✅ **FIXED:** Added session cleanup
- ✅ **FIXED:** Proper ComfyUI priming wait

**Minimum Specs:**
- GPU: RTX 3060 12GB
- RAM: 16GB
- Storage: 50GB

**Recommended Specs:**
- GPU: RTX 4070 12GB
- RAM: 32GB
- Storage: 100GB SSD

**Optimal Performance:**
- Enable all optimizations
- Use recommended specs
- Monitor memory usage
- Restart services if slowdown occurs
