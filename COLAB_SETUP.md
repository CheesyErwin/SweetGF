# 🌸 SweetGF - Google Colab Deployment Guide

This guide will help you run SweetGF on Google Colab with free GPU access.

## 📋 Prerequisites

1. **Google Account** - For Google Colab access
2. **Ngrok Account** - Free account for public URL ([Sign up here](https://ngrok.com))
3. **Model Files** - You'll need to provide URLs or upload models

## 🚀 Quick Start

### Option 1: Upload Notebook to Colab

1. Open [Google Colab](https://colab.research.google.com)
2. Click **File → Upload notebook**
3. Upload `SweetGF_Colab.ipynb`
4. Change runtime to GPU: **Runtime → Change runtime type → GPU (T4)**
5. Run cells in order

### Option 2: Direct Upload

1. Open [Google Colab](https://colab.research.google.com)
2. Create a new notebook
3. Copy-paste cells from `SweetGF_Colab.ipynb`
4. Change runtime to GPU
5. Run cells in order

## 📝 Setup Steps

### 1. Get Ngrok Auth Token

1. Go to [ngrok.com](https://ngrok.com) and sign up (free)
2. Go to [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken)
3. Copy your authtoken
4. Paste it when prompted in the notebook

### 2. Upload Your Files

**Method A: From GitHub (Recommended)**
- Push your SweetGF code to GitHub
- Modify cell 2 to clone your repo:
  ```python
  !git clone https://github.com/yourusername/SweetGF.git /content/SweetGF
  ```

**Method B: Manual Upload**
- In Colab, click the folder icon on the left
- Create folder `/content/SweetGF`
- Upload `app.py`, `requirements.txt`, and `static/` folder

### 3. Model Files

You have several options for models:

**Option A: Use Smaller Models (Fastest)**
```python
# In cell 5, use:
MODEL = "phi3:mini"  # Only 2.3GB, fast
```

**Option B: Use Better Models**
```python
# In cell 5, use:
MODEL = "llama2:7b"  # 4.1GB, better quality
MODEL = "mistral:7b"  # 4.1GB, good balance
```

**For ComfyUI Models:**
- You'll need to provide download URLs in cell 7
- Or upload models manually to `/content/ComfyUI/models/`
- Required models:
  - Checkpoint: `waiNSFWIllustrious_v110.safetensors` (or any SD1.5/SDXL model)
  - LoRA: `Better_detailed_pussy_and_anus_v3.0.safetensors` (optional)
  - ControlNet: `control_v11p_sd15_openpose_fp16.safetensors` (optional)

### 4. Run the App

1. Run all cells in order (1-11)
2. Wait for installations (5-10 minutes first time)
3. Get your public URL from cell 11
4. Access the app in your browser
5. Run cell 13 to keep it alive

## ⚙️ Configuration

### Disable Image Generation (Faster Setup)

If you only want chat functionality:

1. Skip cell 6-8 (ComfyUI installation)
2. The app will work with chat only
3. Image generation buttons will show as unavailable

### Use Different Models

Edit the `.env` configuration in cell 9:

```python
# For faster responses:
OLLAMA_MODEL=phi3:mini

# For better quality:
OLLAMA_MODEL=mistral:7b

# Disable features to save resources:
ENABLE_FACE_DETAILER=false
ENABLE_LORA=false
```

## 🔧 Troubleshooting

### "Ollama not responding"
```python
# Run in a new cell:
!pkill ollama
!ollama serve &
!sleep 5
!ollama list
```

### "ComfyUI not responding"
```python
# Run in a new cell:
%cd /content/ComfyUI
!pkill -f "python main.py"
!python main.py --listen 0.0.0.0 --port 8188 &
```

### "Out of memory"
- Use smaller models (phi3:mini)
- Disable face detailer and LoRA
- Restart runtime: **Runtime → Restart runtime**

### "Session disconnected"
- Colab free tier has usage limits
- Keep the tab active
- Run cell 13 to keep alive
- Consider Colab Pro for longer sessions

## 💡 Tips

### For Free Tier Users

1. **Use smaller models** - phi3:mini is fast and works well
2. **Disable optional features** - Turn off face detailer and LoRA
3. **Keep tab active** - Colab disconnects inactive sessions
4. **Save conversations** - They're lost when session ends

### For Better Performance

1. **Colab Pro** - Longer sessions, better GPUs
2. **Persistent storage** - Mount Google Drive to save models
3. **Pre-download models** - Store in Drive, copy to Colab

### Saving Models to Google Drive

Add this cell after cell 1:

```python
from google.colab import drive
drive.mount('/content/drive')

# Create model directory in Drive
!mkdir -p /content/drive/MyDrive/ComfyUI_Models

# Link to ComfyUI
!ln -s /content/drive/MyDrive/ComfyUI_Models /content/ComfyUI/models
```

## 📊 Resource Usage

### Minimal Setup (Chat Only)
- **RAM**: ~4GB
- **GPU**: Not required (can use CPU)
- **Storage**: ~5GB
- **Setup time**: ~5 minutes

### Full Setup (Chat + Images)
- **RAM**: ~12GB
- **GPU**: T4 or better (free tier)
- **Storage**: ~15GB
- **Setup time**: ~15 minutes

## 🔒 Security Notes

1. **Ngrok URL is public** - Anyone with the URL can access your app
2. **No authentication** - Consider adding password protection
3. **Session data** - Cleared when Colab session ends
4. **API keys** - Don't commit to public repos

## 🆘 Getting Help

If you encounter issues:

1. Check cell 12 to verify all services are running
2. Look at the troubleshooting section above
3. Check Colab's output for error messages
4. Restart runtime and try again

## 📱 Sharing Your App

Your ngrok URL is public and shareable:
- Share with friends (they can access simultaneously)
- URL changes each time you restart
- Free tier has connection limits

## ⏱️ Session Limits

**Colab Free:**
- 12 hours maximum session
- Disconnects after 90 minutes idle
- Limited GPU hours per week

**Colab Pro:**
- 24 hours maximum session
- Better GPUs available
- More GPU hours

## 🎯 Next Steps

After successful setup:

1. Customize Luna's personality in `app.py`
2. Add more features
3. Deploy to a permanent server (Hugging Face Spaces, Railway, etc.)
4. Set up proper authentication

---

Made with 💕 for cloud deployment
