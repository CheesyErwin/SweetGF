#!/usr/bin/env python3
"""
SweetGF Quick Setup for Google Colab
Run this script to automatically set up everything.
"""

import os
import sys
import subprocess
import time
import json

def run_command(cmd, description, check=True):
    """Run a shell command with status output"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    print(f"✅ {description} - Done!")
    return True

def check_service(url, name, timeout=5):
    """Check if a service is running"""
    try:
        import requests
        response = requests.get(url, timeout=timeout)
        print(f"✅ {name}: Running (Status {response.status_code})")
        return True
    except Exception as e:
        print(f"❌ {name}: Not responding - {str(e)}")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║           🌸 SweetGF - Colab Quick Setup 🌸          ║
    ║                                                       ║
    ║     Automated setup for Google Colab deployment      ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    # Check if running in Colab
    try:
        import google.colab
        IN_COLAB = True
        print("✅ Running in Google Colab")
    except:
        IN_COLAB = False
        print("⚠️  Not running in Colab - some features may not work")
    
    # Step 1: Install system dependencies
    if not run_command(
        "apt-get update -qq && apt-get install -y -qq wget git python3-pip",
        "Installing system dependencies"
    ):
        return
    
    # Step 2: Install Python packages
    if not run_command(
        "pip install -q flask flask-cors requests python-dotenv pyngrok",
        "Installing Python packages"
    ):
        return
    
    # Step 3: Install Ollama
    print("\n" + "="*60)
    print("🤖 Installing Ollama")
    print("="*60)
    if not os.path.exists("/usr/local/bin/ollama"):
        run_command("curl -fsSL https://ollama.com/install.sh | sh", "Downloading Ollama")
    else:
        print("✅ Ollama already installed")
    
    # Step 4: Start Ollama
    print("\n" + "="*60)
    print("🚀 Starting Ollama server")
    print("="*60)
    subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(5)
    print("✅ Ollama server started")
    
    # Step 5: Pull model
    print("\n" + "="*60)
    print("📥 Downloading AI model")
    print("="*60)
    print("Choose a model:")
    print("1. phi3:mini (2.3GB) - Fastest, good for testing")
    print("2. mistral:7b (4.1GB) - Better quality")
    print("3. llama2:7b (4.1GB) - Balanced")
    
    choice = input("\nEnter choice (1-3) [default: 1]: ").strip() or "1"
    
    models = {
        "1": "phi3:mini",
        "2": "mistral:7b",
        "3": "llama2:7b"
    }
    
    model = models.get(choice, "phi3:mini")
    print(f"\n📦 Pulling {model}... This may take a few minutes.")
    run_command(f"ollama pull {model}", f"Downloading {model}")
    
    # Step 6: Setup ComfyUI (optional)
    print("\n" + "="*60)
    print("🎨 ComfyUI Setup")
    print("="*60)
    setup_comfy = input("Install ComfyUI for image generation? (y/n) [default: n]: ").strip().lower()
    
    comfyui_installed = False
    if setup_comfy == 'y':
        if not os.path.exists('/content/ComfyUI'):
            run_command(
                "git clone https://github.com/comfyanonymous/ComfyUI.git /content/ComfyUI",
                "Cloning ComfyUI"
            )
            run_command(
                "cd /content/ComfyUI && pip install -q -r requirements.txt && pip install -q xformers",
                "Installing ComfyUI dependencies"
            )
        
        # Create model directories
        os.makedirs('/content/ComfyUI/models/checkpoints', exist_ok=True)
        os.makedirs('/content/ComfyUI/models/loras', exist_ok=True)
        os.makedirs('/content/ComfyUI/models/controlnet', exist_ok=True)
        
        # Start ComfyUI
        print("\n🚀 Starting ComfyUI server...")
        subprocess.Popen(
            ['python', '/content/ComfyUI/main.py', '--listen', '0.0.0.0', '--port', '8188'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(10)
        comfyui_installed = True
        print("✅ ComfyUI server started")
        print("\n⚠️  Note: You need to upload models to /content/ComfyUI/models/checkpoints/")
    
    # Step 7: Setup SweetGF
    print("\n" + "="*60)
    print("🌸 Setting up SweetGF")
    print("="*60)
    
    # Create .env file
    env_content = f"""# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL={model}

# ComfyUI Configuration
COMFYUI_BASE_URL=http://127.0.0.1:8188
COMFYUI_PATH=/content/ComfyUI

# App Configuration
FLASK_PORT=5000
FLASK_DEBUG=False

# Startup Optimization
PRIME_COMFYUI_DEEP=false

# FaceDetailer Configuration
ENABLE_FACE_DETAILER=false

# LoRA Configuration
ENABLE_LORA=false

# ControlNet Configuration
CONTROLNET_MODEL=control_v11p_sd15_openpose_fp16.safetensors
CONTROLNET_STRENGTH=0.8
"""
    
    with open('/content/SweetGF/.env', 'w') as f:
        f.write(env_content)
    
    print("✅ Environment configured")
    
    # Step 8: Setup ngrok
    print("\n" + "="*60)
    print("🌐 Setting up public access")
    print("="*60)
    print("\nTo access your app publicly, you need an ngrok auth token.")
    print("Get one free at: https://dashboard.ngrok.com/get-started/your-authtoken")
    
    ngrok_token = input("\nEnter your ngrok auth token (or press Enter to skip): ").strip()
    
    if ngrok_token:
        from pyngrok import ngrok, conf
        conf.get_default().auth_token = ngrok_token
        print("✅ Ngrok configured")
    else:
        print("⚠️  Skipping ngrok - app will only be accessible locally")
    
    # Step 9: Start Flask app
    print("\n" + "="*60)
    print("🚀 Starting SweetGF application")
    print("="*60)
    
    os.chdir('/content/SweetGF')
    
    # Start Flask in background
    import threading
    def run_flask():
        os.system('python app.py')
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    time.sleep(5)
    
    # Create ngrok tunnel if token provided
    if ngrok_token:
        from pyngrok import ngrok
        public_url = ngrok.connect(5000, bind_tls=True)
        
        print("\n" + "="*60)
        print("🎉 SUCCESS! SweetGF is now running!")
        print("="*60)
        print(f"\n🌐 Public URL: {public_url}")
        print("\n💡 Share this URL with anyone to access your app")
    else:
        print("\n" + "="*60)
        print("🎉 SUCCESS! SweetGF is running locally!")
        print("="*60)
        print("\n🌐 Local URL: http://localhost:5000")
    
    # Step 10: Check services
    print("\n" + "="*60)
    print("🔍 Checking services")
    print("="*60)
    time.sleep(2)
    
    check_service("http://localhost:11434", "Ollama")
    if comfyui_installed:
        check_service("http://localhost:8188", "ComfyUI")
    check_service("http://localhost:5000/api/health", "SweetGF")
    
    print("\n" + "="*60)
    print("✅ Setup Complete!")
    print("="*60)
    print("\n📝 Next steps:")
    print("   1. Open the URL in your browser")
    print("   2. Start chatting with Luna!")
    if comfyui_installed:
        print("   3. Upload models to /content/ComfyUI/models/checkpoints/ for image generation")
    print("\n⚠️  Keep this script running to maintain the connection")
    print("\n" + "="*60)
    
    # Keep alive
    try:
        print("\n💤 Keeping session alive... (Press Ctrl+C to stop)")
        while True:
            time.sleep(60)
            print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down...")

if __name__ == "__main__":
    main()
