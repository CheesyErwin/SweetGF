# 🚀 SweetGF Colab - Quick Start

## 3 Ways to Deploy

### 🟢 Option 1: Simple Notebook (Easiest)
**Best for: Beginners**

1. Upload `SweetGF_Colab_Simple.ipynb` to [Google Colab](https://colab.research.google.com)
2. Change runtime to GPU (Runtime → Change runtime type → GPU)
3. Run cells 1-6 in order
4. Get your public URL
5. Done! ✨

**Time:** ~10 minutes  
**Complexity:** ⭐ Easy

---

### 🟡 Option 2: Full Notebook (Most Features)
**Best for: Full control**

1. Upload `SweetGF_Colab.ipynb` to [Google Colab](https://colab.research.google.com)
2. Change runtime to GPU
3. Run all 13 cells
4. Customize settings as needed
5. Get your public URL

**Time:** ~15 minutes  
**Complexity:** ⭐⭐ Medium

---

### 🔵 Option 3: Quick Setup Script (Automated)
**Best for: Command-line users**

1. Upload your files to Colab
2. Run:
   ```python
   !python colab_quick_setup.py
   ```
3. Follow prompts
4. Done!

**Time:** ~8 minutes  
**Complexity:** ⭐ Easy

---

## 📋 What You Need

### Required
- ✅ Google account (for Colab)
- ✅ Ngrok account (free) - [Sign up](https://ngrok.com)
- ✅ Your SweetGF files

### Optional
- 🎨 ComfyUI models (for image generation)
- 💾 Google Drive (for persistent storage)
- 💰 Colab Pro (for longer sessions)

---

## ⚡ Quick Commands

### Get Ngrok Token
```
https://dashboard.ngrok.com/get-started/your-authtoken
```

### Clone from GitHub
```python
!git clone https://github.com/yourusername/SweetGF.git /content/SweetGF
```

### Check Services
```python
!curl http://localhost:11434  # Ollama
!curl http://localhost:8188   # ComfyUI
!curl http://localhost:5000   # SweetGF
```

### Restart Everything
```python
!pkill ollama && ollama serve &
!pkill -f "python main.py" && cd /content/ComfyUI && python main.py --listen 0.0.0.0 --port 8188 &
!pkill -f "python app.py" && cd /content/SweetGF && python app.py &
```

---

## 🎯 Recommended Models

### For Chat (Ollama)

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| `phi3:mini` | 2.3GB | ⚡⚡⚡ | ⭐⭐ | Testing, free tier |
| `mistral:7b` | 4.1GB | ⚡⚡ | ⭐⭐⭐ | Balanced |
| `llama2:7b` | 4.1GB | ⚡⚡ | ⭐⭐⭐ | General use |

### For Images (ComfyUI)

- **Anime**: waiNSFWIllustrious, AnythingV5
- **Realistic**: Realistic Vision, DreamShaper
- **NSFW**: Specific NSFW models (18+ only)

---

## 💡 Pro Tips

### Save Resources
```python
# Use smallest model
MODEL = "phi3:mini"

# Disable optional features
ENABLE_FACE_DETAILER=false
ENABLE_LORA=false
```

### Persistent Storage
```python
# Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Store models in Drive
!mkdir -p /content/drive/MyDrive/SweetGF_Models
!ln -s /content/drive/MyDrive/SweetGF_Models /content/ComfyUI/models
```

### Keep Session Alive
```python
# Install extension
!pip install colabcode

# Or use JavaScript
from IPython.display import display, Javascript
display(Javascript('''
  function KeepAlive(){
    console.log("Keeping alive");
    document.querySelector("colab-connect-button").click()
  }
  setInterval(KeepAlive, 60000)
'''))
```

---

## 🔥 Common Issues

### "Out of Memory"
- Use `phi3:mini` model
- Disable face detailer and LoRA
- Restart runtime

### "Session Disconnected"
- Keep tab active
- Run keep-alive cell
- Consider Colab Pro

### "Ollama Not Responding"
```python
!pkill ollama
!ollama serve &
!sleep 5
!ollama list
```

### "Models Not Found"
```python
# Check model directory
!ls -lh /content/ComfyUI/models/checkpoints/

# Download model (example)
!wget -O /content/ComfyUI/models/checkpoints/model.safetensors "URL"
```

---

## 📊 Resource Usage

### Chat Only (Minimal)
- **RAM**: 4GB
- **GPU**: Optional
- **Storage**: 5GB
- **Time**: 5 min

### Chat + Images (Full)
- **RAM**: 12GB
- **GPU**: T4 (free tier)
- **Storage**: 15GB
- **Time**: 15 min

---

## 🎓 Next Steps

After successful deployment:

1. **Customize** - Edit `app.py` for personality
2. **Add Models** - Upload better models
3. **Secure** - Add authentication
4. **Scale** - Deploy to permanent hosting
5. **Share** - Give URL to friends

---

## 📚 Full Documentation

- **Setup Guide**: `COLAB_SETUP.md`
- **Full Notebook**: `SweetGF_Colab.ipynb`
- **Simple Notebook**: `SweetGF_Colab_Simple.ipynb`
- **Quick Script**: `colab_quick_setup.py`
- **Main README**: `README.md`

---

## 🆘 Need Help?

1. Check `COLAB_SETUP.md` for detailed troubleshooting
2. Run the status check cell
3. Check Colab output for errors
4. Verify all files are uploaded
5. Try restarting runtime

---

## ⚠️ Important Notes

- **Free Tier Limits**: 12 hours max, 90 min idle disconnect
- **Public URL**: Anyone with URL can access
- **No Auth**: Add password protection for security
- **Session Data**: Lost when runtime ends
- **GPU Hours**: Limited per week on free tier

---

Made with 💕 for easy Colab deployment
