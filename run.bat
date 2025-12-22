@echo off
chcp 65001 >nul
title Safe UserBot - Run Script

echo =========================================
echo 🚀 Safe UserBot - Professional & Safe
echo 👨‍💻 Developer: RANA
echo 📧 Contact: ranaeditz333@gmail.com
echo =========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.7+
    pause
    exit /b 1
)

python -c "import sys; exit(0) if sys.version_info >= (3, 7) else exit(1)" >nul 2>&1
if errorlevel 1 (
    echo ❌ Python 3.7+ required
    pause
    exit /b 1
)

REM Check requirements.txt
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)

REM Check config.py
if not exist "config.py" (
    echo ❌ config.py not found. Please run setup.py first
    pause
    exit /b 1
)

REM Create directories
if not exist "data" mkdir data
if not exist "sessions" mkdir sessions
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

echo ✓ Directories created

REM Install/update dependencies
echo 📦 Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✓ Dependencies installed

REM Backup session
if exist "sessions\main_account.session" (
    if not exist "backups\sessions" mkdir backups\sessions
    copy "sessions\main_account.session" "backups\sessions\main_account_%date:~10,4%%date:~4,2%%date:~7,2%_%time:~0,2%%time:~3,2%.session" >nul
    echo ✓ Session backed up
)

REM Set Python path
set PYTHONPATH=%cd%

REM Run bot
echo.
echo 🚀 Starting bot...
echo.

:restart
python main.py
if errorlevel 0 (
    echo.
    echo ✓ Bot stopped normally
    pause
    goto :end
) else (
    echo.
    echo ❌ Bot crashed with error code %errorlevel%
    
    REM Check for session error (exit code 2)
    if %errorlevel% equ 2 (
        echo ⚠ Session error detected. Trying to recover...
        del "sessions\main_account.session" 2>nul
    )
    
    echo.
    echo 🔄 Restarting in 10 seconds...
    echo Press Ctrl+C to stop
    timeout /t 10 /nobreak >nul
    goto :restart
)

:end
pause