# 🌸 SweetGF Colab - Cheatsheet

## 🚀 Quick Deploy (3 Steps)

```
1. Upload notebook → 2. Enable GPU → 3. Run cells → Done!
```

---

## 📁 Files You Need

```
Essential:
├── app.py                          ← Main app
├── requirements.txt                ← Dependencies
└── static/                         ← Frontend
    └── index.html

For Colab:
├── SweetGF_Colab_Simple.ipynb     ← Quick setup
├── SweetGF_Colab.ipynb            ← Full setup
└── requirements-colab.txt          ← Colab deps
```

---

## ⚡ One-Liners

### Clone from GitHub
```python
!git clone https://github.com/user/SweetGF.git /content/SweetGF
```

### Install Everything
```python
!pip install -q flask flask-cors requests python-dotenv pyngrok
```

### Start Ollama
```python
!curl -fsSL https://ollama.com/install.sh | sh && ollama serve &
```

### Pull Model
```python
!ollama pull phi3:mini  # or mistral:7b, llama2:7b
```

### Start ComfyUI
```python
!git clone https://github.com/comfyanonymous/ComfyUI /content/ComfyUI
!cd /content/ComfyUI && pip install -q -r requirements.txt
!python /content/ComfyUI/main.py --listen 0.0.0.0 --port 8188 &
```

### Create Public URL
```python
from pyngrok import ngrok
public_url = ngrok.connect(5000)
print(public_url)
```

---

## 🎯 Model Sizes

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| phi3:mini | 2.3GB | ⚡⚡⚡ | ⭐⭐ |
| mistral:7b | 4.1GB | ⚡⚡ | ⭐⭐⭐ |
| llama2:7b | 4.1GB | ⚡⚡ | ⭐⭐⭐ |

---

## 🔧 Essential Commands

### Check Status
```python
!curl http://localhost:11434        # Ollama
!curl http://localhost:8188         # ComfyUI
!curl http://localhost:5000         # SweetGF
```

### Restart Services
```python
!pkill ollama && ollama serve &
!pkill -f "python main.py" && cd /content/ComfyUI && python main.py --listen 0.0.0.0 &
!pkill -f "python app.py" && cd /content/SweetGF && python app.py &
```

### Check Resources
```python
!nvidia-smi                         # GPU
!free -h                            # RAM
!df -h                              # Disk
```

### List Models
```python
!ollama list                        # Ollama models
!ls /content/ComfyUI/models/checkpoints/  # ComfyUI models
```

---

## 📝 Environment Variables

### Minimal Config
```env
OLLAMA_MODEL=phi3:mini
FLASK_PORT=5000
ENABLE_FACE_DETAILER=false
ENABLE_LORA=false
```

### Full Config
```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=/content/ComfyUI
FLASK_PORT=5000
FLASK_DEBUG=False
ENABLE_FACE_DETAILER=true
ENABLE_LORA=true
CONTROLNET_MODEL=control_v11p_sd15_openpose_fp16.safetensors
CONTROLNET_STRENGTH=0.8
```

---

## 🐛 Quick Fixes

### Out of Memory
```python
# Use smaller model
!ollama pull phi3:mini

# Disable features in .env
ENABLE_FACE_DETAILER=false
ENABLE_LORA=false
```

### Service Not Responding
```python
# Restart everything
!pkill ollama && ollama serve &
!sleep 5
!ollama pull phi3:mini
```

### Can't Access URL
```python
# Check ngrok token
from pyngrok import conf
print(conf.get_default().auth_token)

# Recreate tunnel
from pyngrok import ngrok
ngrok.kill()
public_url = ngrok.connect(5000)
print(public_url)
```

### Session Timeout
```python
# Keep alive
import time
while True:
    time.sleep(60)
    print(".", end="", flush=True)
```

---

## 💾 Google Drive Integration

### Mount Drive
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Save Models to Drive
```python
# Create directory
!mkdir -p /content/drive/MyDrive/SweetGF_Models

# Link to ComfyUI
!ln -s /content/drive/MyDrive/SweetGF_Models /content/ComfyUI/models
```

### Backup Code
```python
# Backup to Drive
!cp -r /content/SweetGF /content/drive/MyDrive/SweetGF_Backup
```

---

## 🔐 Add Password Protection

### Quick Auth
```python
# In app.py, add:
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

users = {"admin": "password123"}

@auth.verify_password
def verify(username, password):
    if username in users and users[username] == password:
        return username

@app.route('/')
@auth.login_required
def index():
    return send_from_directory('static', 'index.html')
```

---

## 📊 Resource Requirements

### Chat Only
```
RAM:     4GB
GPU:     Optional
Storage: 5GB
Time:    5 min
```

### Chat + Images
```
RAM:     12GB
GPU:     T4 (free tier)
Storage: 15GB
Time:    15 min
```

---

## 🎨 Download Models

### ComfyUI Checkpoint
```python
# Example (replace URL)
!wget -O /content/ComfyUI/models/checkpoints/model.safetensors \
  "https://huggingface.co/user/model/resolve/main/model.safetensors"
```

### LoRA
```python
!wget -O /content/ComfyUI/models/loras/lora.safetensors \
  "YOUR_LORA_URL"
```

### ControlNet
```python
!wget -O /content/ComfyUI/models/controlnet/controlnet.safetensors \
  "YOUR_CONTROLNET_URL"
```

---

## 🌐 Ngrok Setup

### Get Token
```
https://dashboard.ngrok.com/get-started/your-authtoken
```

### Set Token
```python
from pyngrok import ngrok, conf
conf.get_default().auth_token = "YOUR_TOKEN"
```

### Create Tunnel
```python
public_url = ngrok.connect(5000, bind_tls=True)
print(f"Access at: {public_url}")
```

---

## 🎯 Optimization Tips

### Speed
- Use `phi3:mini`
- Disable face detailer
- Disable LoRA
- Skip ComfyUI

### Quality
- Use `mistral:7b`
- Enable all features
- Better ComfyUI models
- More generation steps

### Resources
- Chat-only mode
- Smallest model
- Use Drive for storage
- Colab Pro

---

## 📱 Sharing

### Your URL
```
https://xxxx.ngrok-free.app
```

### Share With
- Friends (simultaneous access)
- Anyone with link
- Changes on restart

### Limits
- Free tier: connection limits
- Colab: 12h max session
- Ngrok: bandwidth limits

---

## ⏱️ Session Limits

### Free Tier
```
Max:    12 hours
Idle:   90 minutes
GPU:    Limited hours/week
```

### Colab Pro
```
Max:    24 hours
GPUs:   A100, V100
Hours:  More per week
```

---

## 🆘 Emergency Commands

### Nuclear Restart
```python
# Kill everything
!pkill -9 ollama
!pkill -9 python

# Restart runtime
# Runtime → Restart runtime

# Start over
!ollama serve &
!cd /content/SweetGF && python app.py &
```

### Check Everything
```python
# Processes
!ps aux | grep -E "ollama|python|comfy"

# Ports
!netstat -tulpn | grep -E "5000|8188|11434"

# Logs
!journalctl -u ollama -n 50
```

---

## 🎓 Learning Resources

- [Colab Docs](https://colab.research.google.com/notebooks/intro.ipynb)
- [Ollama Docs](https://ollama.ai/docs)
- [ComfyUI GitHub](https://github.com/comfyanonymous/ComfyUI)
- [Flask Docs](https://flask.palletsprojects.com/)
- [Ngrok Docs](https://ngrok.com/docs)

---

## ✅ Checklist

### Before Deploy
- [ ] Files ready
- [ ] GPU enabled
- [ ] Ngrok token
- [ ] Model chosen

### After Deploy
- [ ] Services running
- [ ] URL accessible
- [ ] Chat working
- [ ] Keep-alive running

---

## 🎉 Success Indicators

```
✅ Ollama: Running (200)
✅ ComfyUI: Running (200)
✅ SweetGF: Running (200)
✅ Public URL: https://xxxx.ngrok-free.app
✅ Chat: Responding
✅ Images: Generating
```

---

**Quick Start:** Upload `SweetGF_Colab_Simple.ipynb` → Enable GPU → Run cells → Done! 🚀
