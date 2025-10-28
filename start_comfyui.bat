@echo off
echo ========================================
echo   Starting ComfyUI (Portable)
echo ========================================
echo.

set COMFYUI_PATH=D:\ComfyUI_windows_portable

if not exist "%COMFYUI_PATH%" (
    echo [ERROR] ComfyUI not found at: %COMFYUI_PATH%
    echo Please update the COMFYUI_PATH variable in this script
    pause
    exit /b 1
)

cd /d "%COMFYUI_PATH%"

echo Starting ComfyUI from: %COMFYUI_PATH%
echo ComfyUI will be available at: http://127.0.0.1:8188
echo.

REM Check if it's the portable version with run_nvidia_gpu.bat
if exist "run_nvidia_gpu.bat" (
    echo Detected portable version with NVIDIA GPU...
    call run_nvidia_gpu.bat
) else if exist "run_cpu.bat" (
    echo Detected portable version with CPU mode...
    call run_cpu.bat
) else if exist "main.py" (
    echo Detected standard installation...
    python main.py
) else (
    echo [ERROR] Could not find ComfyUI startup script
    pause
    exit /b 1
)
