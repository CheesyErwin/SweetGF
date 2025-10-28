# ComfyUI Optimization Guide

## Prevent Model Loading/Unloading

ComfyUI may unload models from VRAM to save memory. Here's how to keep models loaded for faster generation:

### Method 1: Command Line Arguments (Recommended)

Start ComfyUI with these arguments to keep models in VRAM:

```bash
# Windows (run_nvidia_gpu.bat)
python main.py --gpu-only --highvram

# Or for lower VRAM systems (8GB+)
python main.py --normalvram
```

**Arguments explained:**
- `--gpu-only`: Keep models in GPU VRAM only (fastest)
- `--highvram`: Don't move models to RAM (requires 12GB+ VRAM)
- `--normalvram`: Balance between VRAM and RAM (8GB+ VRAM)
- `--lowvram`: For 6GB VRAM cards
- `--novram`: CPU only (slowest)

### Method 2: Edit ComfyUI Startup Script

**For Windows:**

Edit `run_nvidia_gpu.bat` in your ComfyUI folder:

```batch
@echo off

.\python_embeded\python.exe -s ComfyUI\main.py --gpu-only --highvram --listen 0.0.0.0 --port 8188

pause
```

**For Linux/Mac:**

Edit the startup script or run:

```bash
python main.py --gpu-only --highvram --listen 0.0.0.0 --port 8188
```

### Method 3: Environment Variable

Set in your `.env` file:

```env
COMFYUI_VRAM_MANAGEMENT=gpu-only
```

Then modify ComfyUI startup to use this setting.

### Additional Optimizations

**1. Use Consistent Checkpoint**
- The app uses `waiNSFWIllustrious_v110.safetensors` by default
- Don't switch checkpoints to avoid reload delays
- Place checkpoint in: `ComfyUI/models/checkpoints/`

**2. Disable Auto-Unload**
- ComfyUI Settings → Performance
- Increase "Model Unload Delay" to maximum (or disable)

**3. Increase VRAM Allocation**
- Close other GPU-intensive apps
- Ensure ComfyUI has priority access to VRAM

**4. Use FP16 Models**
- Half-precision models use less VRAM
- Faster loading and generation
- Minimal quality loss

### Recommended Setup for SweetGF

**For 12GB+ VRAM (RTX 3060 12GB, RTX 4070, etc.):**
```bash
python main.py --gpu-only --highvram --listen 0.0.0.0 --port 8188
```

**For 8GB VRAM (RTX 3060 Ti, RTX 4060, etc.):**
```bash
python main.py --normalvram --listen 0.0.0.0 --port 8188
```

**For 6GB VRAM (GTX 1060, RTX 3050, etc.):**
```bash
python main.py --lowvram --listen 0.0.0.0 --port 8188
```

### Verify It's Working

After starting ComfyUI with these settings:

1. Generate one image
2. Check GPU memory usage (stays high)
3. Generate another image (should be faster - no reload)
4. Monitor console - no "Loading checkpoint..." messages between generations

### Performance Comparison

**Without optimization:**
- First image: 15-30 seconds
- Second image: 15-30 seconds (model reloads)
- Third image: 15-30 seconds (model reloads)

**With optimization:**
- First image: 15-30 seconds (initial load)
- Second image: 5-10 seconds (model stays loaded)
- Third image: 5-10 seconds (model stays loaded)

### Troubleshooting

**Out of Memory Errors:**
- Use `--normalvram` instead of `--highvram`
- Reduce image size (512x512 instead of 768x768)
- Close other GPU applications

**Still Reloading:**
- Check ComfyUI console for errors
- Ensure you're using the same checkpoint
- Verify command line arguments are applied
- Restart ComfyUI with new settings

### SweetGF Configuration

The app is already configured to use consistent settings:
- ✅ Same checkpoint for all generations
- ✅ Consistent model parameters
- ✅ No checkpoint switching
- ✅ Optimized workflow structure

Just configure ComfyUI startup as shown above!
