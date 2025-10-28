# ComfyUI Setup Guide

This app works with **both portable and standard ComfyUI installations**.

## Installation Types

### Option 1: Portable Installation (Windows)

**Download:**
- Get ComfyUI portable from: https://github.com/comfyanonymous/ComfyUI/releases
- Extract to any folder (e.g., `D:\ComfyUI_windows_portable`)

**Configuration:**
```env
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=D:\ComfyUI_windows_portable
```

**Start ComfyUI:**
```bash
cd D:\ComfyUI_windows_portable
run_nvidia_gpu.bat
```

### Option 2: Standard Installation (All Platforms)

**Install via Git:**
```bash
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip install -r requirements.txt
```

**Configuration:**
```env
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=C:\Users\YourName\ComfyUI
# Or on Linux/Mac: /home/username/ComfyUI
```

**Start ComfyUI:**
```bash
cd ComfyUI
python main.py
```

## Required Models

Place these models in your ComfyUI installation:

### 1. Checkpoint (Required)
```
File: waiNSFWIllustrious_v110.safetensors
Location: ComfyUI/models/checkpoints/
Download: https://civitai.com/models/...
```

### 2. LoRA (Optional - for anatomical detail)
```
File: Better_detailed_pussy_and_anus_v3.0.safetensors
Location: ComfyUI/models/loras/
Download: https://civitai.com/models/...
Toggle: ENABLE_LORA=true/false in .env
```

### 3. Face Detection Model (Optional - for FaceDetailer)
```
File: face_yolov8n.pt
Location: ComfyUI/models/ultralytics/bbox/
Download: https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt
Toggle: ENABLE_FACE_DETAILER=true/false in .env
```

### 4. ComfyUI-Impact-Pack (Optional - for FaceDetailer)
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git
cd ComfyUI-Impact-Pack
pip install -r requirements.txt
```

## Configuration

### Minimal Setup (Just ComfyUI URL)

If you only need the API connection:

```env
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=
```

The app will work fine without `COMFYUI_PATH` set.

### Full Setup (With Path)

If you need file system operations:

**Portable:**
```env
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=D:\ComfyUI_windows_portable
```

**Standard (Windows):**
```env
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=C:\Users\YourName\ComfyUI
```

**Standard (Linux/Mac):**
```env
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=/home/username/ComfyUI
```

## Verification

### 1. Check ComfyUI is Running

Open browser: http://127.0.0.1:8188

You should see the ComfyUI interface.

### 2. Check API Connection

The SweetGF app will show on startup:
```
🎨 ComfyUI: http://127.0.0.1:8188
📁 ComfyUI Path: D:\ComfyUI_windows_portable (if set)
🎭 FaceDetailer: Enabled/Disabled
🎨 LoRA: Enabled/Disabled
```

### 3. Test Generation

Try generating a profile picture in the app. Check ComfyUI console for:
```
Prompt received
Loading checkpoint...
Generating image...
```

## Troubleshooting

### ComfyUI Not Detected

**Problem:** App can't connect to ComfyUI

**Solution:**
1. Make sure ComfyUI is running
2. Check the URL is correct: `http://127.0.0.1:8188`
3. Try `http://localhost:8188` instead
4. Check firewall isn't blocking port 8188

### Models Not Found

**Problem:** "Checkpoint not found" or "LoRA not found"

**Solution:**
1. Check model files are in correct folders
2. Verify exact filenames match in `app.py`:
   - `COMFYUI_CHECKPOINT = "waiNSFWIllustrious_v110.safetensors"`
   - `COMFYUI_LORA = "Better_detailed_pussy_and_anus_v3.0.safetensors"`
3. Restart ComfyUI after adding models

### FaceDetailer Not Working

**Problem:** "FaceDetailer node not found"

**Solution:**
1. Install ComfyUI-Impact-Pack (see above)
2. Download face detection model to `ultralytics/bbox/`
3. Restart ComfyUI completely
4. Or disable: `ENABLE_FACE_DETAILER=false`

### Slow Generation

**Problem:** First image takes 30+ seconds

**Solution:**
1. Enable deep priming: `PRIME_COMFYUI_DEEP=true`
2. Keep ComfyUI running between generations
3. Use `--highvram` or `--normalvram` when starting ComfyUI
4. See `COMFYUI_OPTIMIZATION.md` for more tips

## Different Ports

If ComfyUI runs on a different port:

```env
# ComfyUI on port 8189
COMFYUI_BASE_URL=http://127.0.0.1:8189

# ComfyUI on remote server
COMFYUI_BASE_URL=http://192.168.1.100:8188
```

## Summary

✅ **Both portable and standard installations work**  
✅ **Only URL is required** - path is optional  
✅ **Same configuration** for both types  
✅ **Models go in same folders** regardless of installation type  

The app communicates via HTTP API, so it doesn't matter which installation type you use!
