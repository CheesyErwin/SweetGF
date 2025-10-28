# 🌸 SweetGF - Wholesome Virtual Girlfriend Experience

A wholesome AI companion app that combines Ollama for natural conversations and ComfyUI for image generation.

## ✨ Features

- 💬 **Natural Conversations**: Chat with Luna, a caring AI girlfriend powered by Ollama
- 🎨 **Image Generation**: Generate custom images using ComfyUI
- 💕 **Wholesome Personality**: Supportive, empathetic, and genuinely caring responses
- 🧠 **Conversation Memory**: Remembers your chat within each session
- 🎯 **Clean UI**: Beautiful, modern interface with gradient themes
- ⚡ **Real-time Status**: Shows connection status for Ollama and ComfyUI

## 📋 Prerequisites

Before running this app, you need to have:

1. **Python 3.8+** installed
2. **Ollama** installed and running ([Download](https://ollama.ai))
3. **ComfyUI** (optional, for image generation) ([GitHub](https://github.com/comfyanonymous/ComfyUI))

### Setting up Ollama

1. Install Ollama from https://ollama.ai
2. Pull a model (recommended: llama2, mistral, or neural-chat):
   ```bash
   ollama pull llama2
   ```
3. Ollama will automatically start on `http://localhost:11434`

### Setting up ComfyUI (Optional)

You have ComfyUI portable at `D:\ComfyUI_windows_portable`.

1. Start ComfyUI:
   ```bash
   # Use the provided helper script:
   start_comfyui.bat
   
   # Or start manually:
   cd D:\ComfyUI_windows_portable
   run_nvidia_gpu.bat  # For NVIDIA GPU
   # or
   run_cpu.bat         # For CPU mode
   ```

2. Verify you have models:
   - Check `D:\ComfyUI_windows_portable\models\checkpoints\`
   - Download models if needed (SD XL, anime models, etc.)
   - Place `.safetensors` files in the checkpoints folder

3. ComfyUI will run on `http://127.0.0.1:8188`

## 🚀 Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd d:\Pyth\SweetGF
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** (copy from `.env.example`):
   ```bash
   copy .env.example .env
   ```

4. **Edit `.env` file** if needed to match your configuration:
   ```
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   COMFYUI_BASE_URL=http://localhost:8188
   FLASK_PORT=5000
   FLASK_DEBUG=True
   ```

## 🎮 Usage

1. **Make sure Ollama is running**:
   ```bash
   ollama serve
   ```

2. **Start the SweetGF application**:
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

4. **Start chatting with Luna!** 💕

## 🎨 Using Image Generation

To use the image generation feature:

1. Make sure ComfyUI is running
2. Click the "🎨 Generate Image" button in the chat interface
3. Describe the appearance you'd like (e.g., "pink hair, blue eyes, wearing a cozy sweater")
4. Check ComfyUI's output folder for the generated image

## 🛠️ Configuration

### Changing the AI Model

Edit the `.env` file and change `OLLAMA_MODEL` to your preferred model:
```
OLLAMA_MODEL=mistral        # Good for general conversation
OLLAMA_MODEL=neural-chat    # Optimized for chat
OLLAMA_MODEL=llama2         # Balanced performance
```

### Customizing Luna's Personality

Edit the `GIRLFRIEND_SYSTEM_PROMPT` in `app.py` to customize Luna's personality traits and behavior.

### Adjusting Image Generation

Modify the `ComfyUIClient.generate_image()` method in `app.py` to:
- Change image dimensions (width/height)
- Adjust generation steps and CFG scale
- Modify the prompt enhancement
- Use different models or samplers

## 📁 Project Structure

```
SweetGF/
├── app.py                 # Flask backend with Ollama & ComfyUI integration
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── .env                  # Your environment configuration (create this)
├── README.md             # This file
└── static/
    └── index.html        # Frontend web interface
```

## 🔧 API Endpoints

- `GET /` - Main web interface
- `GET /api/health` - Health check and service status
- `POST /api/chat` - Send a chat message
  ```json
  {
    "message": "Hello!",
    "session_id": "optional-session-id"
  }
  ```
- `POST /api/generate-image` - Generate an image
  ```json
  {
    "prompt": "pink hair, blue eyes"
  }
  ```
- `POST /api/conversation/clear` - Clear conversation history
  ```json
  {
    "session_id": "session-id"
  }
  ```

## 💡 Tips

- **First message might be slow**: The first response takes longer as Ollama loads the model
- **Use specific prompts**: For image generation, be specific about what you want
- **Session persistence**: Each browser tab maintains its own conversation session
- **Memory is session-based**: Conversations are stored in memory and cleared on restart

## 🎯 Recommended Models

### For Conversation (Ollama):
- `llama2` - Balanced, good general conversation
- `mistral` - Fast and coherent
- `neural-chat` - Optimized for chat scenarios
- `openchat` - Very friendly and conversational

### For Images (ComfyUI):
- Stable Diffusion XL - High quality, versatile
- Anime models (if you prefer anime-style avatars)
- Realistic Vision - For photorealistic images

## 🐛 Troubleshooting

**Issue**: "Ollama API error" or status shows disconnected
- Make sure Ollama is running: `ollama serve`
- Check if the model is downloaded: `ollama list`
- Verify the URL in `.env` matches your Ollama installation

**Issue**: "ComfyUI API error" or status shows disconnected
- Make sure ComfyUI is running: `python main.py`
- Verify ComfyUI is accessible at `http://localhost:8188`
- Check if you have models in the `models/checkpoints/` folder

**Issue**: Slow responses
- Some models are large and may take time to generate responses
- Try a smaller/faster model like `mistral` or `neural-chat`
- Ensure your system has enough RAM (8GB+ recommended)

**Issue**: Image generation fails
- Verify you have a model in ComfyUI's checkpoint folder
- Check the workflow matches your ComfyUI setup
- Look at ComfyUI's console for error messages

## 🤝 Contributing

Feel free to customize Luna's personality, improve the UI, or add new features!

## 📝 License

This project is open source and available for personal use.

## ⚠️ Disclaimer

This is a virtual AI companion for entertainment and companionship. Always maintain healthy real-world relationships and social connections.

---

Made with 💕 for a wholesome AI companion experience
