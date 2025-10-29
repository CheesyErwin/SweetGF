# Resource Management: ComfyUI vs Ollama Optimization

## The Problem

**Resource Competition:**
- **ComfyUI:** Uses GPU VRAM + GPU compute + RAM
- **Ollama:** Uses GPU VRAM + GPU compute + RAM (or CPU if no GPU)
- **Both running simultaneously:** Fighting for same resources

### Typical Resource Usage

**ComfyUI (Image Generation):**
- GPU VRAM: 8-12GB
- GPU Compute: 95-100% utilization
- RAM: 4-8GB
- Duration: 8-15 seconds per image

**Ollama (Text Generation):**
- GPU VRAM: 6-10GB (7B model)
- GPU Compute: 80-95% utilization
- RAM: 8-12GB
- Duration: 5-10 seconds per response

**Total Simultaneous:**
- GPU VRAM: 14-22GB (exceeds most GPUs!)
- GPU Compute: 175-195% (impossible!)
- RAM: 12-20GB

## Current Issues

### 1. VRAM Overflow
**Symptom:** `CUDA out of memory` errors

**Cause:**
- ComfyUI loads checkpoint: 10GB VRAM
- Ollama loads model: 8GB VRAM
- Total: 18GB > RTX 4070's 12GB

**Result:**
- One service crashes
- Both services slow down (swapping to RAM)
- Generation fails

### 2. GPU Compute Contention
**Symptom:** Both services slow down when running together

**Cause:**
- ComfyUI needs 100% GPU for fast generation
- Ollama needs 80% GPU for fast inference
- Both compete for same compute units

**Result:**
- Image generation: 15s → 25s (67% slower)
- Text generation: 8s → 15s (87% slower)

### 3. RAM Pressure
**Symptom:** System becomes unresponsive

**Cause:**
- Both services use significant RAM
- OS starts swapping to disk
- Everything slows down

**Result:**
- Entire system lag
- Disk thrashing
- Poor user experience

## Optimization Strategies

### Strategy 1: Sequential Processing (Easiest) ⚡⚡⚡

**Concept:** Never run both at the same time

**Implementation:**
```python
# Add a global lock
import threading
resource_lock = threading.Lock()

# In text generation
def chat_with_ollama(messages):
    with resource_lock:
        # Only one service at a time
        return OllamaClient.chat(messages)

# In image generation
def generate_image(prompt):
    with resource_lock:
        # Only one service at a time
        return ComfyUIClient.generate_image(prompt)
```

**Pros:**
- ✅ Simple to implement
- ✅ No VRAM conflicts
- ✅ Each service gets full GPU
- ✅ Reliable and stable

**Cons:**
- ❌ User must wait for text before image starts
- ❌ Slightly longer total time

**Impact:**
- Text: 5-10s (full speed)
- Image: 8-15s (full speed)
- Total: 13-25s sequential

### Strategy 2: Ollama CPU Mode (Recommended) ⚡⚡⚡⚡

**Concept:** Run Ollama on CPU, ComfyUI on GPU

**Implementation:**
```bash
# Start Ollama without GPU
set CUDA_VISIBLE_DEVICES=-1
ollama serve

# Or in Ollama config
OLLAMA_NUM_GPU=0
```

**Pros:**
- ✅ No resource competition
- ✅ ComfyUI gets full GPU (fast images)
- ✅ Both can run simultaneously
- ✅ No code changes needed

**Cons:**
- ❌ Ollama slower on CPU (10-20s vs 5-10s)
- ❌ Requires good CPU (8+ cores)

**Impact:**
- Text: 10-20s (CPU speed)
- Image: 8-15s (full GPU speed)
- Can run in parallel!

**Best for:** RTX 3060/4070 with good CPU

### Strategy 3: Model Unloading (Moderate) ⚡⚡

**Concept:** Unload Ollama when generating images

**Implementation:**
```python
def unload_ollama():
    """Unload Ollama model from VRAM"""
    requests.post(f"{OLLAMA_BASE_URL}/api/generate", json={
        "model": OLLAMA_MODEL,
        "keep_alive": 0  # Unload immediately
    })

def reload_ollama():
    """Reload Ollama model into VRAM"""
    requests.post(f"{OLLAMA_BASE_URL}/api/generate", json={
        "model": OLLAMA_MODEL,
        "keep_alive": -1  # Keep loaded
    })

# Before image generation
unload_ollama()
generate_image()
reload_ollama()
```

**Pros:**
- ✅ Frees VRAM for ComfyUI
- ✅ No VRAM conflicts
- ✅ Both services available

**Cons:**
- ❌ Reload delay (5-10s)
- ❌ Complex to manage
- ❌ User waits for reload

**Impact:**
- Image: 8-15s (full GPU)
- Reload: 5-10s overhead
- Total: 13-25s per image

### Strategy 4: Smaller Models (Quality Trade-off) ⚡⚡⚡

**Concept:** Use smaller models that fit together

**Implementation:**
```env
# Use smaller Ollama model
OLLAMA_MODEL=llama2:7b  # Instead of 13b or 70b

# Smaller = less VRAM
# 7B model: ~6GB VRAM
# 13B model: ~10GB VRAM
# 70B model: ~40GB VRAM
```

**Pros:**
- ✅ Both fit in VRAM together
- ✅ Can run simultaneously
- ✅ Simple solution

**Cons:**
- ❌ Lower text quality
- ❌ Less capable responses
- ❌ May not meet quality needs

**Impact:**
- VRAM: 6GB (Ollama) + 10GB (ComfyUI) = 16GB
- Still tight on 12GB GPU
- Works on 16GB+ GPU

### Strategy 5: Dynamic GPU Allocation (Advanced) ⚡⚡⚡⚡⚡

**Concept:** Intelligently manage GPU resources

**Implementation:**
```python
class ResourceManager:
    def __init__(self):
        self.current_task = None
        self.lock = threading.Lock()
    
    def request_gpu(self, task_type, priority='normal'):
        """Request GPU access with priority"""
        with self.lock:
            if self.current_task is None:
                self.current_task = task_type
                return True
            
            # High priority can interrupt low priority
            if priority == 'high' and self.current_task_priority == 'low':
                self.interrupt_current_task()
                self.current_task = task_type
                return True
            
            return False  # Must wait
    
    def release_gpu(self):
        """Release GPU for other tasks"""
        with self.lock:
            self.current_task = None

# Usage
resource_manager = ResourceManager()

def generate_image():
    if resource_manager.request_gpu('image', priority='high'):
        try:
            return ComfyUIClient.generate_image()
        finally:
            resource_manager.release_gpu()
    else:
        # Queue or wait
        pass
```

**Pros:**
- ✅ Intelligent resource allocation
- ✅ Priority system
- ✅ Optimal performance
- ✅ Handles edge cases

**Cons:**
- ❌ Complex implementation
- ❌ Requires careful testing
- ❌ More code to maintain

**Impact:**
- Best possible performance
- Adapts to workload
- Prevents conflicts

## Recommended Solution

### For Most Users: Strategy 2 (Ollama CPU Mode)

**Why:**
- Simple to implement
- Reliable and stable
- ComfyUI gets full GPU (images are priority)
- Text generation still fast enough on good CPU

**Setup:**

**1. Configure Ollama for CPU:**

**Windows:**
```powershell
# Create Ollama config
$env:OLLAMA_NUM_GPU = "0"
ollama serve
```

**Or edit Ollama service:**
```
Environment=OLLAMA_NUM_GPU=0
```

**Linux:**
```bash
# Add to ~/.bashrc or service file
export OLLAMA_NUM_GPU=0
ollama serve
```

**2. Verify:**
```bash
# Check Ollama is using CPU
ollama ps
# Should show 0 GPU layers
```

**3. Test:**
- Text generation: Should work (10-20s)
- Image generation: Should be fast (8-15s)
- Both simultaneously: Should work!

### For Power Users: Strategy 5 (Dynamic Allocation)

**Why:**
- Maximum performance
- Intelligent resource management
- Best user experience

**Implementation:** See code example above

## Hybrid Approach (Best of Both Worlds)

**Concept:** Use GPU when available, fall back to CPU

```python
class SmartResourceManager:
    def __init__(self):
        self.gpu_available = True
        self.lock = threading.Lock()
    
    def generate_text(self, messages):
        """Generate text with smart GPU usage"""
        with self.lock:
            if self.gpu_available:
                # Try GPU first
                try:
                    return self._generate_gpu(messages)
                except Exception as e:
                    # Fall back to CPU
                    return self._generate_cpu(messages)
            else:
                # GPU busy, use CPU
                return self._generate_cpu(messages)
    
    def generate_image(self, prompt):
        """Generate image (always GPU, waits if needed)"""
        with self.lock:
            self.gpu_available = False
            try:
                return ComfyUIClient.generate_image(prompt)
            finally:
                self.gpu_available = True
```

## Performance Comparison

### Current (No Optimization)
```
Simultaneous:
- Text: 15s (slow, competing)
- Image: 25s (slow, competing)
- VRAM: Overflowing
- Crashes: Frequent
```

### Strategy 1 (Sequential)
```
Sequential:
- Text: 8s (full speed)
- Image: 12s (full speed)
- Total: 20s (wait for each)
- VRAM: No conflicts
- Crashes: None
```

### Strategy 2 (Ollama CPU) ✅ Recommended
```
Parallel:
- Text: 15s (CPU speed)
- Image: 10s (full GPU)
- Can overlap!
- VRAM: No conflicts
- Crashes: None
```

### Strategy 5 (Dynamic)
```
Intelligent:
- Text: 8s (GPU when available)
- Image: 10s (priority access)
- Optimal scheduling
- VRAM: Managed
- Crashes: None
```

## Implementation Priority

### Phase 1: Quick Fix (5 minutes)

**Run Ollama on CPU:**
```bash
# Stop Ollama
taskkill /F /IM ollama.exe

# Set environment variable
set OLLAMA_NUM_GPU=0

# Restart Ollama
ollama serve
```

**Test:**
- Generate text → Should work
- Generate image → Should be fast
- Both together → Should work!

### Phase 2: Sequential Lock (30 minutes)

**Add to app.py:**
```python
import threading

# Global resource lock
resource_lock = threading.Lock()

# Wrap Ollama calls
def chat_with_lock(messages):
    with resource_lock:
        return OllamaClient.chat(messages)

# Wrap ComfyUI calls
def generate_image_with_lock(prompt):
    with resource_lock:
        return ComfyUIClient.generate_image(prompt)
```

### Phase 3: Smart Management (2-4 hours)

**Implement ResourceManager class**
- Priority system
- Dynamic allocation
- Fallback strategies
- Monitoring and logging

## Monitoring Resource Usage

### Check GPU Usage

**Windows:**
```powershell
# Real-time GPU monitoring
nvidia-smi -l 1
```

**Look for:**
- VRAM usage per process
- GPU utilization %
- Temperature

### Check RAM Usage

**Windows:**
```powershell
# Task Manager
tasklist /FI "IMAGENAME eq python.exe"
tasklist /FI "IMAGENAME eq ollama.exe"
```

### Optimal Targets

**GPU (RTX 4070 12GB):**
- ComfyUI: 10-11GB VRAM (when generating)
- Ollama: 0GB VRAM (CPU mode)
- Total: 10-11GB / 12GB ✅

**RAM (32GB system):**
- ComfyUI: 6GB
- Ollama: 10GB
- Flask: 1GB
- OS: 8GB
- Total: 25GB / 32GB ✅

## Troubleshooting

### Issue: Still Getting OOM Errors

**Solution:**
1. Verify Ollama is using CPU: `ollama ps`
2. Check VRAM: `nvidia-smi`
3. Reduce image resolution
4. Disable FaceDetailer temporarily

### Issue: Text Generation Too Slow on CPU

**Solution:**
1. Upgrade CPU (8+ cores recommended)
2. Use smaller model (7B instead of 13B)
3. Implement Strategy 1 (sequential)
4. Get more VRAM (upgrade GPU)

### Issue: Both Services Crash

**Solution:**
1. Check total RAM usage
2. Close other applications
3. Increase system RAM
4. Use sequential processing

## Hardware Recommendations

### Minimum (Budget)
- GPU: RTX 3060 12GB
- RAM: 16GB
- CPU: 6-core
- **Strategy:** Ollama CPU mode + reduced settings

### Recommended (Balanced)
- GPU: RTX 4070 12GB
- RAM: 32GB
- CPU: 8-core
- **Strategy:** Ollama CPU mode + full settings

### Optimal (No Compromises)
- GPU: RTX 4090 24GB
- RAM: 64GB
- CPU: 12-core
- **Strategy:** Both on GPU + dynamic allocation

## Summary

**The Problem:**
- ComfyUI and Ollama compete for GPU resources
- Causes slowdowns, crashes, OOM errors

**Best Solution:**
- **Run Ollama on CPU** (Strategy 2)
- ComfyUI gets full GPU
- Text generation still fast enough
- No resource conflicts

**Quick Fix:**
```bash
set OLLAMA_NUM_GPU=0
ollama serve
```

**Expected Results:**
- ✅ No more VRAM conflicts
- ✅ Stable image generation
- ✅ Reliable text generation
- ✅ Can run simultaneously

**Alternative:**
- Add sequential lock (Strategy 1)
- Simpler but slower
- Good for low-end hardware
