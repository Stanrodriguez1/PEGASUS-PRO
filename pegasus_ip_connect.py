#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║           PEGASUS PRO — IP Connect Launcher              ║
║        No USB Required · No Cable · Works Over Internet  ║
╚══════════════════════════════════════════════════════════╝

Supported Modes:
  [1] Direct IP Connect    → Instant connect using saved/new IP (No pairing code)
  [2] Android 11+ Pairing  → One-time pairing (keys cached permanently)
  [3] Different Network    → Connect over internet (WAN / Tunnel)
  [4] NVIDIA AI Assistant  → Control device with natural language prompts
"""

import os
import sys
import time
import json
import subprocess
import socket
import platform

# ──────────────────────────────────────────────────────────
# Try importing colorama; install hint if missing
# ──────────────────────────────────────────────────────────
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] colorama not found. Run:  pip install -r requirements.txt")
    sys.exit(1)

# ──────────────────────────────────────────────────────────
# Constants & Config
# ──────────────────────────────────────────────────────────
PEGASUS_MAIN        = "pegasus_v_1.3.py"
CONFIG_FILE         = os.path.expanduser("~/.pegasus_device_cache.json")
ADB_DEFAULT_PORT    = 5555
CONNECT_TIMEOUT_SEC = 10
MAX_RETRY           = 3

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    clear()
    print(Fore.CYAN + Style.BRIGHT + """
██████╗ ███████╗ ██████╗  █████╗ ███████╗██╗   ██╗███████╗
██╔══██╗██╔════╝██╔════╝ ██╔══██╗██╔════╝██║   ██║██╔════╝
██████╔╝█████╗  ██║  ███╗███████║███████╗██║   ██║███████╗
██╔═══╝ ██╔══╝  ██║   ██║██╔══██║╚════██║██║   ██║╚════██║
██║     ███████╗╚██████╔╝██║  ██║███████║╚██████╔╝███████║
╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
""")
    print(Fore.GREEN + Style.BRIGHT + "          ⚡  IP Connect & AI Launcher  ⚡")
    print(Fore.WHITE + "     No USB · Direct IP Auto-Connect · NVIDIA AI Mode\n")
    print(Fore.CYAN  + "─" * 60)

def load_cached_devices() -> list[dict]:
    """Load previously connected devices."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_device_to_cache(ip: str, port: int, label: str = ""):
    """Save an IP and port to the local cache so codes are never needed again."""
    devices = load_cached_devices()
    # Check if already exists
    for dev in devices:
        if dev.get("ip") == ip and dev.get("port") == port:
            return
    devices.append({"ip": ip, "port": port, "label": label or f"{ip}:{port}", "last_used": time.strftime("%Y-%m-%d %H:%M")})
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(devices, f, indent=2)
    except Exception:
        pass

def run_adb(args: list, timeout: int = CONNECT_TIMEOUT_SEC) -> tuple[int, str, str]:
    """Run an adb command. Returns (returncode, stdout, stderr)."""
    try:
        result = subprocess.run(
            ["adb"] + args,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except FileNotFoundError:
        return -1, "", "ADB not found. Please install ADB and add it to PATH."
    except subprocess.TimeoutExpired:
        return -1, "", f"ADB command timed out after {timeout}s."

def check_adb_installed() -> bool:
    code, out, err = run_adb(["version"])
    if code == -1:
        print(Fore.RED + f"\n  ✗  {err}")
        print(Fore.YELLOW + "\n  Install ADB:")
        print("    Windows  → winget install Google.PlatformTools")
        print("    macOS    → brew install android-platform-tools")
        print("    Linux    → sudo apt install adb\n")
        return False
    version_line = out.splitlines()[0] if out else "ADB"
    print(Fore.GREEN + f"  ✔  {version_line}")
    return True

def adb_kill_restart_server():
    run_adb(["kill-server"])
    time.sleep(1)
    run_adb(["start-server"])
    time.sleep(1)

def is_ip_reachable(ip: str, port: int = ADB_DEFAULT_PORT, timeout: float = 3.0) -> bool:
    """Quick TCP probe."""
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError):
        return False

def connected_devices() -> list[str]:
    """Return list of currently connected ADB device serials."""
    code, out, _ = run_adb(["devices"])
    devices = []
    for line in out.splitlines()[1:]:
        if "\tdevice" in line:
            devices.append(line.split("\t")[0].strip())
    return devices

def print_ok(text: str):
    print(Fore.GREEN + f"  ✔  {text}")

def print_err(text: str):
    print(Fore.RED + f"  ✗  {text}")

def print_info(text: str):
    print(Fore.YELLOW + f"  ℹ  {text}")

def prompt(msg: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    val = input(Fore.YELLOW + f"\n  ➤  {msg}{hint}: " + Fore.WHITE).strip()
    return val if val else default

def launch_main_tool():
    """Hand off to the main Pegasus launcher after connection."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path  = os.path.join(script_dir, PEGASUS_MAIN)

    if not os.path.exists(main_path):
        print_err(f"Main tool not found: {PEGASUS_MAIN}")
        print_info("Make sure pegasus_v_1.3.py is in the same folder.")
        sys.exit(1)

    print(Fore.CYAN + "\n" + "─" * 60)
    print(Fore.GREEN + Style.BRIGHT + "\n  🚀  Launching PEGASUS PRO...\n")
    time.sleep(1)

    python = sys.executable
    os.execv(python, [python, main_path])

# ──────────────────────────────────────────────────────────
# Modes
# ──────────────────────────────────────────────────────────

def mode_direct_ip():
    """Direct IP connect without any pairing code requirements."""
    print(Fore.CYAN + "\n" + "─" * 60)
    print(Fore.GREEN + Style.BRIGHT + "  MODE 1 — Direct IP Connection (No Code)")
    print(Fore.CYAN + "─" * 60)

    cached = load_cached_devices()
    if cached:
        print(Fore.YELLOW + "\n  Saved Recent Devices:")
        for idx, dev in enumerate(cached, 1):
            print(f"    [{idx}] {dev.get('label')} (Last used: {dev.get('last_used', 'N/A')})")
        print("    [N] Enter New IP Address")
        
        choice = prompt("Select device or Enter 'N'", "1")
        if choice.isdigit() and 1 <= int(choice) <= len(cached):
            selected = cached[int(choice) - 1]
            ip = selected["ip"]
            port = selected["port"]
        else:
            ip = prompt("Enter device IP address (e.g. 192.168.1.42)")
            port_str = prompt("ADB port", str(ADB_DEFAULT_PORT))
            port = int(port_str) if port_str.isdigit() else ADB_DEFAULT_PORT
    else:
        ip = prompt("Enter device IP address (e.g. 192.168.1.42)")
        port_str = prompt("ADB port", str(ADB_DEFAULT_PORT))
        port = int(port_str) if port_str.isdigit() else ADB_DEFAULT_PORT

    if not ip:
        print_err("No IP provided.")
        return False

    print_info(f"Connecting to {ip}:{port}...")
    code, out, err = run_adb(["connect", f"{ip}:{port}"])
    output = (out + err).lower()

    if "connected" in output or "already connected" in output:
        print_ok(f"Successfully connected to {ip}:{port}!")
        save_device_to_cache(ip, port)
        return True
    else:
        print_err(f"Connection failed: {out or err}")
        print_info("Make sure Wireless Debugging / TCP ADB is active on the target device.")
        return False

def mode_pair():
    """Android 11+ Initial Pairing (One-time only)."""
    print(Fore.CYAN + "\n" + "─" * 60)
    print(Fore.GREEN + Style.BRIGHT + "  MODE 2 — Android 11+ One-Time Wireless Pairing")
    print(Fore.CYAN + "─" * 60)
    print(Fore.WHITE + """
  On your Android phone:
    Settings → Developer Options → Wireless Debugging → ON
    Tap 'Pair device with pairing code'
""")
    pair_ip   = prompt("Enter IP address shown on phone")
    pair_port = prompt("Enter PAIRING PORT shown on phone")
    pair_code = prompt("Enter 6-digit pairing code")

    if not all([pair_ip, pair_port, pair_code]):
        print_err("Missing required pairing fields.")
        return False

    print_info(f"Pairing with {pair_ip}:{pair_port}...")
    code, out, err = run_adb(["pair", f"{pair_ip}:{pair_port}", pair_code])
    output = (out + err).lower()

    if "successfully paired" in output or "paired" in output:
        print_ok("Pairing successful! Key saved permanently.")
        connect_port = prompt("Enter CONNECT PORT shown at top of Wireless Debugging screen")
        if connect_port:
            run_adb(["connect", f"{pair_ip}:{connect_port}"])
            save_device_to_cache(pair_ip, int(connect_port))
            return True
    else:
        print_err(f"Pairing failed: {out or err}")
    return False

def mode_wan():
    """WAN/Internet connection."""
    print(Fore.CYAN + "\n" + "─" * 60)
    print(Fore.GREEN + Style.BRIGHT + "  MODE 3 — Different Network / Internet (WAN)")
    print(Fore.CYAN + "─" * 60)
    public_ip   = prompt("Enter Public IP / ngrok Host")
    public_port = prompt("Enter Public Port")

    if not public_ip or not public_port:
        print_err("Incomplete details.")
        return False

    print_info(f"Connecting to {public_ip}:{public_port}...")
    code, out, err = run_adb(["connect", f"{public_ip}:{public_port}"])
    output = (out + err).lower()
    if "connected" in output or "already connected" in output:
        print_ok(f"Connected to {public_ip}:{public_port}")
        save_device_to_cache(public_ip, int(public_port), label="WAN Remote")
        return True
    else:
        print_err(f"Connection failed: {out or err}")
        return False

def mode_ai():
    """Launch NVIDIA AI Assistant."""
    try:
        import ai_agent
        ai_agent.run_ai_interactive()
    except ImportError:
        print_err("ai_agent.py module not found.")

# ──────────────────────────────────────────────────────────
# Main Loop
# ──────────────────────────────────────────────────────────

def main_menu():
    banner()
    if not check_adb_installed():
        sys.exit(1)

    existing = connected_devices()
    if existing:
        print_ok(f"Currently active device: {', '.join(existing)}")

    while True:
        print(Fore.CYAN + "\n" + "─" * 60)
        print(Fore.GREEN + Style.BRIGHT + "  SELECT AN OPTION\n")
        print(Fore.WHITE  + "    [1]  Direct IP Connect          (Quick connect, no code needed)")
        print(Fore.WHITE  + "    [2]  Initial Wireless Pairing   (Android 11+ one-time setup)")
        print(Fore.WHITE  + "    [3]  WAN / Internet Connect     (Remote via Public IP or ngrok)")
        print(Fore.MAGENTA+ "    [4]  🤖 NVIDIA AI Assistant     (Natural language ADB control)")
        print(Fore.YELLOW + "    [5]  Launch PEGASUS PRO Suite   (Open main menu directly)")
        print(Fore.RED    + "    [0]  Exit")
        print(Fore.CYAN   + "─" * 60)

        choice = prompt("Enter choice", "1").strip()
        success = False

        if choice == "1":
            success = mode_direct_ip()
        elif choice == "2":
            success = mode_pair()
        elif choice == "3":
            success = mode_wan()
        elif choice == "4":
            mode_ai()
            continue
        elif choice == "5":
            launch_main_tool()
        elif choice == "0":
            print(Fore.YELLOW + "\n  Goodbye!\n")
            sys.exit(0)
        else:
            print_err("Invalid choice.")
            continue

        if success:
            print(Fore.CYAN + "\n" + "─" * 60)
            print_ok("Device ready!")
            print(Fore.CYAN + "─" * 60)
            go = prompt("Launch PEGASUS PRO tool suite now? (y/n)", "y").lower()
            if go in ["y", "yes", ""]:
                launch_main_tool()

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n  Exiting.\n")
        sys.exit(0)
