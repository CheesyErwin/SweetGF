@echo off
echo ========================================
echo   SweetGF Setup Script
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [2/4] Creating .env file...
if not exist .env (
    copy .env.example .env
    echo Created .env file from template
) else (
    echo .env file already exists, skipping
)

echo.
echo [3/4] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not running or not installed
    echo Please install Ollama from: https://ollama.ai
    echo After installation, run: ollama pull llama2
) else (
    echo Ollama is running!
)

echo.
echo [4/4] Checking ComfyUI...
if exist "D:\ComfyUI_windows_portable" (
    echo ComfyUI portable installation found at D:\ComfyUI_windows_portable
    echo You can start it with: start_comfyui.bat
) else (
    echo [INFO] ComfyUI not found (optional for image generation)
)

curl -s http://127.0.0.1:8188/system_stats >nul 2>&1
if not errorlevel 1 (
    echo ComfyUI is currently running!
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To start the application, run:
echo   python app.py
echo.
echo Then open your browser to:
echo   http://localhost:5000
echo.
pause
