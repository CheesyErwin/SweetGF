# FaceDetailer Setup Guide

FaceDetailer (from ComfyUI-Impact-Pack) is now integrated to automatically improve face quality with a second refinement pass.

## What FaceDetailer Does

- **Detects faces** in generated images using YOLO
- **Crops face region** and upscales it
- **Runs second generation pass** on face only (denoise: 0.4)
- **Blends refined face** back into original image
- **Result:** Better face details, eyes, and overall facial quality

## Installation

### 1. Install ComfyUI-Impact-Pack (includes FaceDetailer)

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git
cd ComfyUI-Impact-Pack
pip install -r requirements.txt
```

### 2. Download Required Models

**Face Detection Model (Required):**
```
Download: face_yolov8n.pt
Place in: ComfyUI/models/ultralytics/bbox/
URL: https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8n.pt
```

**Alternative Models (Optional):**
- `face_yolov8s.pt` - More accurate but slower
- `face_yolov8m.pt` - Best accuracy, slowest

### 3. Restart ComfyUI

After installing, restart ComfyUI completely:
```bash
# Stop ComfyUI (Ctrl+C)
# Start again
run_nvidia_gpu.bat
```

## Configuration

The app uses these FaceDetailer settings:

```python
"bbox_detector": "face_yolov8n.pt"  # Face detection model
"bbox_threshold": 0.5                # Detection confidence
"denoise": 0.4                       # Refinement strength (0.3-0.5)
"steps": 20                          # Refinement steps
"cfg": 8.0                           # Guidance scale
"feather": 5                         # Blend smoothness
```

### Adjusting Face Refinement Strength

Edit `app.py` and change the `denoise` value in both FaceDetailer nodes:

**Light refinement (subtle):**
```python
"denoise": 0.3
```

**Medium refinement (default):**
```python
"denoise": 0.4
```

**Strong refinement (may change face more):**
```python
"denoise": 0.5
```

## Performance Impact

**Without FaceDetailer:**
- Generation time: ~5-10 seconds
- Face quality: Variable

**With FaceDetailer:**
- Generation time: ~8-15 seconds (+3-5 seconds)
- Face quality: Consistently better

## Troubleshooting

### Error: "FaceDetailer node not found"
- Install ComfyUI-Impact-Pack
- Restart ComfyUI completely
- Check custom_nodes folder has Impact-Pack

### Error: "face_yolov8n.pt not found"
- Download the model from HuggingFace
- Place in `ComfyUI/models/ultralytics/bbox/`
- Create folders if they don't exist

### Faces not being detected
- Lower `bbox_threshold` to 0.3 (more sensitive)
- Try `face_yolov8s.pt` for better detection
- Check if face is visible in image

### Faces look over-processed
- Lower `denoise` to 0.3
- Reduce `cfg` to 7.0
- Increase `feather` to 10 for smoother blend

### Generation too slow
- Use `face_yolov8n.pt` (fastest)
- Reduce `steps` to 15
- Consider disabling for INTIMATE images if speed is critical

## Disabling FaceDetailer

If you want to disable face refinement:

1. Edit `app.py`
2. Find both FaceDetailer nodes (node "10" and "12")
3. Change SaveImage inputs back to:
   ```python
   "inputs": {"filename_prefix": "luna", "images": ["8", 0]}
   ```
4. Remove the FaceDetailer and UltralyticsDetectorProvider nodes from workflow

## Verification

To verify FaceDetailer is working:

1. Generate an image
2. Check ComfyUI console for:
   ```
   [FaceDetailer] Detected 1 face(s)
   [FaceDetailer] Processing face 1/1
   [FaceDetailer] Face refinement complete
   ```
3. Compare face quality with/without FaceDetailer

## Recommended Setup

**For best results:**
- ✅ Use `face_yolov8n.pt` (good balance)
- ✅ Keep `denoise: 0.4` (default)
- ✅ Keep `steps: 20` (quality)
- ✅ Use `--highvram` or `--normalvram` in ComfyUI
- ✅ Ensure checkpoint stays loaded (see COMFYUI_OPTIMIZATION.md)

**The face quality should now be consistently better across all generated images!** 🎨✨
