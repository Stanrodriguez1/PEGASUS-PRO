@echo off
REM PEGASUS PRO — Automated Windows Setup Script

echo ==================================================
echo       ⚡ PEGASUS PRO AUTOMATED SETUP (WINDOWS) ⚡
echo ==================================================

echo.
echo [*] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found. Installing Python via winget...
    winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements
) else (
    echo [✓] Python is installed.
)

echo.
echo [*] Checking ADB installation...
adb version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ADB not found. Installing Platform Tools via winget...
    winget install Google.PlatformTools --accept-package-agreements --accept-source-agreements
) else (
    echo [✓] ADB is installed.
)

echo.
echo [*] Installing Python requirements...
pip install -r requirements.txt

echo.
echo ==================================================
echo  [✓] Setup Complete!
echo.
echo  To launch PEGASUS PRO:
echo     python pegasus_ip_connect.py
echo ==================================================
pause
