#!/usr/bin/env bash
# PEGASUS PRO — Automated Setup Script (macOS / Linux / Termux)

set -e

echo "=================================================="
echo "      ⚡ PEGASUS PRO AUTOMATED SETUP ⚡"
echo "=================================================="

# Detect OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)
        if [ -n "${TERMUX_VERSION}" ]; then
            PLATFORM="Termux"
        else
            PLATFORM="Linux"
        fi
        ;;
    Darwin*)
        PLATFORM="macOS"
        ;;
    *)
        PLATFORM="Unknown"
        ;;
esac

echo "[*] Detected Platform: ${PLATFORM}"

# 1. Install System Dependencies & ADB
if [ "${PLATFORM}" = "macOS" ]; then
    if ! command -v brew >/dev/null 2>&1; then
        echo "[!] Homebrew not found. Please install Homebrew: https://brew.sh"
    else
        echo "[*] Installing ADB and dependencies via Homebrew..."
        brew install android-platform-tools python3 scrcpy || true
    fi
elif [ "${PLATFORM}" = "Linux" ]; then
    if command -v apt-get >/dev/null 2>&1; then
        echo "[*] Updating apt and installing ADB..."
        sudo apt-get update -y
        sudo apt-get install -y python3 python3-pip adb scrcpy
    elif command -v pacman >/dev/null 2>&1; then
        echo "[*] Installing via pacman..."
        sudo pacman -Sy --noconfirm python android-tools scrcpy
    fi
elif [ "${PLATFORM}" = "Termux" ]; then
    echo "[*] Installing packages for Termux..."
    pkg update -y
    pkg install -y python android-tools git
fi

# 2. Install Python Dependencies
echo "[*] Installing Python dependencies..."
python3 -m pip install --upgrade pip || pip install --upgrade pip || true
pip3 install -r requirements.txt || pip install -r requirements.txt

echo ""
echo "=================================================="
echo " [✓] Installation complete!"
echo ""
echo " To start PEGASUS PRO with IP connection & AI assistant:"
echo "    python3 pegasus_ip_connect.py"
echo "=================================================="
