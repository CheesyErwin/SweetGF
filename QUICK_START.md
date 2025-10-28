# 🚀 Quick Start Guide

## Fastest Way to Get Started

### Option 1: Automated Setup (Windows)
1. Double-click `setup.bat` to install dependencies
2. Install and start Ollama:
   - Download from https://ollama.ai
   - Run: `ollama pull llama2`
3. Start everything:
   - **Easy way**: Double-click `start_all.bat` (starts ComfyUI + SweetGF)
   - **Or just SweetGF**: Double-click `run.bat`
4. Open http://localhost:5000 in your browser

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Create config file
copy .env.example .env

# Install and start Ollama
# Download from https://ollama.ai, then:
ollama pull llama2

# Start the app
python app.py
```

## 🎯 Essential Commands

### Ollama Commands
```bash
# Pull a model
ollama pull llama2

# List installed models
ollama list

# Start Ollama server (if not auto-started)
ollama serve
```

### Try Different Models
```bash
ollama pull mistral          # Faster responses
ollama pull neural-chat      # Better at conversations
ollama pull openchat         # Very friendly
```

Then update `.env`:
```
OLLAMA_MODEL=mistral
```

## 💬 First Conversation

Once the server is running:

1. Open http://localhost:5000
2. Wait for both status indicators to be green
3. Type a message like:
   - "Hi! How are you today?"
   - "Tell me about yourself"
   - "What do you like to do?"

## 🎨 Image Generation (Optional)

You have ComfyUI portable installed at `D:\ComfyUI_windows_portable`.

To enable image generation:

1. Start ComfyUI using the provided script:
   ```bash
   # Double-click this file:
   start_comfyui.bat
   
   # Or start it manually from ComfyUI folder:
   cd D:\ComfyUI_windows_portable
   run_nvidia_gpu.bat  # or run_cpu.bat
   ```

2. Make sure you have a model:
   - Check `D:\ComfyUI_windows_portable\models\checkpoints\`
   - Download Stable Diffusion XL or anime models if needed
   - Place `.safetensors` files in the checkpoints folder

3. Wait for ComfyUI to start (check http://127.0.0.1:8188)

4. In SweetGF, click "🎨 Generate Image" and describe what you want!

## ⚡ Performance Tips

**Slow first response?**
- First message loads the model (10-30 seconds)
- Subsequent messages are much faster

**Want faster responses?**
- Use `mistral` or `openchat` models
- They're smaller and faster than `llama2`

**Out of memory?**
- Try a smaller model
- Close other applications
- Recommended: 8GB+ RAM

## 🔍 Troubleshooting

### "Ollama disconnected"
```bash
# Check if Ollama is running
ollama list

# If not, start it
ollama serve
```

### "ComfyUI disconnected"
```bash
# Start ComfyUI using the provided script
start_comfyui.bat

# Or manually:
cd D:\ComfyUI_windows_portable
run_nvidia_gpu.bat
```

### Port already in use
Edit `.env` and change:
```
FLASK_PORT=5001
```

## 🎉 You're Ready!

Everything should work now. Enjoy chatting with Luna! 💕

---

**Need help?** Check the full README.md for detailed documentation.
