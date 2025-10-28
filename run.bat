@echo off
echo ========================================
echo   Starting SweetGF Server
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [WARNING] .env file not found, creating from template...
    copy .env.example .env
)

echo Starting Flask server...
echo.
python app.py
