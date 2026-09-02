<div align="center">

```
██████╗ ███████╗ ██████╗  █████╗ ███████╗██╗   ██╗███████╗
██╔══██╗██╔════╝██╔════╝ ██╔══██╗██╔════╝██║   ██║██╔════╝
██████╔╝█████╗  ██║  ███╗███████║███████╗██║   ██║███████╗
██╔═══╝ ██╔══╝  ██║   ██║██╔══██║╚════██║██║   ██║╚════██║
██║     ███████╗╚██████╔╝██║  ██║███████║╚██████╔╝███████║
╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
```

# PEGASUS PRO

**Advanced Android Device Management, Wireless Controller & AI Assistant**

[![Python](https://img.shields.io/badge/Python-3.7%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS%20%7C%20Termux-lightgrey?style=for-the-badge)](https://github.com/Stanrodriguez1/PEGASUS-PRO)
[![ADB](https://img.shields.io/badge/Requires-ADB-3DDC84?style=for-the-badge&logo=android&logoColor=white)](https://developer.android.com/tools/adb)
[![NVIDIA AI](https://img.shields.io/badge/NVIDIA-NIM%20AI-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](./LICENSE)

<br/>

> 🛡️ **For Educational, Personal Management & Authorized Device Auditing Only**

</div>

---

## ⚡ Quick Start — Setup On Any Platform

Clone the complete repository to your machine and run the automated setup script:

### 🍏 macOS / 🐧 Linux / 📱 Termux
```bash
git clone https://github.com/Stanrodriguez1/PEGASUS-PRO.git
cd PEGASUS-PRO
chmod +x setup.sh && ./setup.sh
python3 pegasus_ip_connect.py
```

### 🪟 Windows (Command Prompt or PowerShell)
```cmd
git clone https://github.com/Stanrodriguez1/PEGASUS-PRO.git
cd PEGASUS-PRO
setup.bat
python pegasus_ip_connect.py
```

---

## 🤖 NVIDIA AI Assistant Integration

PEGASUS PRO features a natural language AI command assistant powered by **NVIDIA NIM AI Models** (e.g., Llama-3.1 70B Instruct).

### Getting a Free NVIDIA API Key:
1. Visit [build.nvidia.com](https://build.nvidia.com) and create a free developer account.
2. Generate an API Key (starts with `nvapi-...`).
3. Set your key in your terminal or enter it when prompted:
   ```bash
   export NVIDIA_API_KEY="nvapi-your-key-here"
   ```

### What You Can Ask the AI:
* *"Check battery level and device health"*
* *"Take a screenshot and save it locally"*
* *"List third-party installed apps"*
* *"Reboot the device"*
* *"Inspect top CPU consuming processes"*

---

## 📱 Wireless IP Connection (No USB Cable)

### 1. Direct IP Connect (No Repeated Codes)
Once paired or enabled, enter the device's IP to connect instantly:
```
IP: 192.168.1.50
Port: 5555 (default)
```
* **Saved Device Profiles**: The launcher automatically remembers your device history so you can reconnect with 1 click.

### 2. Android 11+ Wireless Debugging (One-Time Initial Pair)
* Go to **Settings > Developer Options > Wireless Debugging > Pair device with pairing code**.
* The launcher pairs and permanently caches the authorization keys on your PC.

### 3. Remote / WAN Connection (Over the Internet)
* Connect to target devices across different networks via public IP/port forwarding or free tunneling (`ngrok tcp <IP>:5555`).

---

## 📋 Comprehensive Feature Breakdown & Requirements

| Option | Feature | Description | Requirements |
|:---|:---|:---|:---|
| **1** | Check Device | Shows Model, Android OS version, and battery percentage | Authorized ADB connection |
| **2** | Connect Device | Connects to device over IP/TCP | Network connectivity |
| **3** | Disconnect | Cleanly disconnects wireless session | Active session |
| **4** | Screen Recording | Records screen and transfers `.mp4` file to local machine | Device storage permission |
| **5** | Screen Mirror | Real-time live screen mirroring on PC | `scrcpy` installed |
| **6** | Show APK List | Lists third-party or all system packages | ADB shell access |
| **7** | Take Screenshot | Grabs instant screenshot and saves to current folder | Storage permission |
| **8** | Power Off | Shuts down device remotely | ADB shell permissions |
| **9** | Install APK | Sideloads any `.apk` file from PC | Package installer permission |
| **10**| Delete APK | Uninstalls specified package name | Package manager permission |
| **11**| Pull File | Downloads file from phone storage to computer | File read permission |
| **12**| Push File | Uploads file from computer to phone storage | File write permission |
| **13**| Send SMS | Dispatches SMS intent | Telephony intent access |
| **14**| Dump Contacts | Exports address book to `.txt` file | Contacts read permission |
| **15**| Reboot Device | Restarts the device | ADB shell |
| **16**| Start App | Launches application package by identifier | Activity manager |
| **17**| Get Logs | Dumps complete `logcat` buffer to disk | Logcat access |
| **18**| Toggle Wi-Fi | Turns device Wi-Fi state on/off | Network management |
| **19**| Check Storage | Displays internal partition capacity & free space | Storage diagnostics |
| **20**| Take Photo | Triggers camera capture intent | Camera access |
| **21**| Troubleshoot | Restarts local ADB server daemon | Local system permissions |
| **22**| Security Audit | Root detection, security patch assessment, open ports | ADB shell |
| **23**| Connection History | Displays session connect/disconnect timestamps | Local log access |

---

## 🔐 License Information
- License Key: `FIREWALLBREAKER`
