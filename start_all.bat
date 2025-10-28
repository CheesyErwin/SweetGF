@echo off
echo ========================================
echo   Starting SweetGF + ComfyUI
echo ========================================
echo.

REM Start ComfyUI in a new window
echo [1/2] Starting ComfyUI...
if exist "D:\ComfyUI_windows_portable\run_nvidia_gpu.bat" (
    start "ComfyUI" cmd /k "cd /d D:\ComfyUI_windows_portable && run_nvidia_gpu.bat"
    echo ComfyUI starting in new window...
) else (
    if exist "D:\ComfyUI_windows_portable\run_cpu.bat" (
        start "ComfyUI" cmd /k "cd /d D:\ComfyUI_windows_portable && run_cpu.bat"
        echo ComfyUI starting in new window ^(CPU mode^)...
    ) else (
        echo [WARNING] ComfyUI not found at D:\ComfyUI_windows_portable
        echo Continuing without ComfyUI...
    )
)

echo.
echo [2/2] Waiting 5 seconds for ComfyUI to initialize...
timeout /t 5 /nobreak >nul

echo.
echo [3/3] Starting SweetGF Flask server...
echo.
python app.py
