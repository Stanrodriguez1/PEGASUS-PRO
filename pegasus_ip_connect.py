#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║           PEGASUS PRO — IP Connect Launcher              ║
║        No USB Required · No Cable · Works Over Internet  ║
╚══════════════════════════════════════════════════════════╝

Supported Modes:
  [1] Same Network / LAN   → Connect via local Wi-Fi IP
  [2] Android 11+ Pairing  → Zero USB, pairing code only
  [3] Different Network    → Connect over internet (WAN)

After a successful connection, the main Pegasus tool
is launched automatically.
"""

import os
import sys
import time
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
# Constants
# ──────────────────────────────────────────────────────────
PEGASUS_MAIN   = "pegasus_v_1.3.py"   # main encrypted launcher
ADB_DEFAULT_PORT     = 5555
ADB_PAIR_PORT_HINT   = 37000          # Android 11+ pairing port (user provides actual)
CONNECT_TIMEOUT_SEC  = 10
MAX_RETRY            = 3

# ──────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────

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
    print(Fore.GREEN + Style.BRIGHT + "          ⚡  IP Connect Launcher  ⚡")
    print(Fore.WHITE + "     No USB · No Cable · Same Network or Internet\n")
    print(Fore.CYAN  + "─" * 60)


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
        print("    Windows  → https://developer.android.com/tools/releases/platform-tools")
        print("    macOS    → brew install android-platform-tools")
        print("    Linux    → sudo apt install adb\n")
        return False
    version_line = out.splitlines()[0] if out else "ADB"
    print(Fore.GREEN + f"  ✔  {version_line}")
    return True


def adb_kill_restart_server():
    print(Fore.YELLOW + "\n  ↻  Restarting ADB server...")
    run_adb(["kill-server"])
    time.sleep(1)
    run_adb(["start-server"])
    time.sleep(1)


def is_ip_reachable(ip: str, port: int = ADB_DEFAULT_PORT, timeout: float = 3.0) -> bool:
    """Quick TCP probe to see if the port is open before trying ADB."""
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


def print_step(num: int, text: str):
    print(Fore.CYAN + f"\n  [{num}] " + Fore.WHITE + text)


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

    # Replace current process with the main tool
    python = sys.executable
    os.execv(python, [python, main_path])


# ══════════════════════════════════════════════════════════
# MODE 1 — Same Network / LAN
# ══════════════════════════════════════════════════════════

def mode_lan():
    """
    Connect to a device on the same Wi-Fi network.

    Android side setup (one time only):
      Developer Options → Wireless debugging → ON
        ─── OR ───
      If ADB USB was used before: run  adb tcpip 5555  while connected via USB.
    """
    print(Fore.CYAN + "\n" + "─" * 60)
    print(Fore.GREEN + Style.BRIGHT + "  MODE 1 — Same Network (LAN / Wi-Fi)")
    print(Fore.CYAN + "─" * 60)

    print(Fore.WHITE + """
  On your Android phone:
    Settings → Developer Options → Wireless Debugging → ON

  Then find your phone's IP address:
    Settings → Wi-Fi → tap your network → IP address
    ─── OR ───
    Settings → About phone → Status → IP address
""")

    ip = prompt("Enter device IP address (e.g. 192.168.1.42)")
    if not ip:
        print_err("No IP entered. Returning to menu.")
        return False

    port_str = prompt("ADB port", str(ADB_DEFAULT_PORT))
    try:
        port = int(port_str)
    except ValueError:
        port = ADB_DEFAULT_PORT

    print_info(f"Probing {ip}:{port}...")
    if not is_ip_reachable(ip, port, timeout=3.0):
        print_err(f"Port {port} not reachable on {ip}.")
        print_info("Make sure Wireless Debugging is enabled and both devices are on the same Wi-Fi.")
        retry = prompt("Retry anyway? (y/n)", "y").lower()
        if retry != "y":
            return False

    print_info(f"Connecting via ADB to {ip}:{port}...")
    code, out, err = run_adb(["connect", f"{ip}:{port}"])

    output = (out + err).lower()
    if "connected" in output or "already connected" in output:
        print_ok(f"Connected to {ip}:{port}")
        devices = connected_devices()
        if devices:
            print_ok(f"Active devices: {', '.join(devices)}")
        return True
    else:
        print_err(f"Connection failed: {out or err}")
        print_info("Try: Developer Options → Wireless Debugging → enabled?")
        return False


# ══════════════════════════════════════════════════════════
# MODE 2 — Android 11+ Wireless Pairing (No USB ever)
# ══════════════════════════════════════════════════════════

def mode_pair():
    """
    Use the Android 11+ wireless debugging pairing code.
    No USB cable is needed at any point.
    """
    print(Fore.CYAN + "\n" + "─" * 60)
    print(Fore.GREEN + Style.BRIGHT + "  MODE 2 — Android 11+ Wireless Pairing (Zero USB)")
    print(Fore.CYAN + "─" * 60)

    print(Fore.WHITE + """
  On your Android 11+ phone:
    Settings → Developer Options → Wireless Debugging → ON
    Tap  "Pair device with pairing code"
    You will see:
       • Wi-Fi Pairing Code  (6-digit number)
       • IP address & Port   (shown below the code)
""")

    pair_ip   = prompt("Enter IP address shown on phone")
    pair_port = prompt("Enter PAIRING PORT shown on phone (e.g. 37000)")
    pair_code = prompt("Enter 6-digit pairing code shown on phone")

    if not all([pair_ip, pair_port, pair_code]):
        print_err("Incomplete information. Returning to menu.")
        return False

    print_info(f"Pairing with {pair_ip}:{pair_port} using code {pair_code}...")
    code, out, err = run_adb(["pair", f"{pair_ip}:{pair_port}", pair_code])

    output = (out + err).lower()
    if "successfully paired" in output or "paired" in output:
        print_ok("Pairing successful!")
    else:
        print_err(f"Pairing failed: {out or err}")
        print_info("Make sure the pairing code has not expired (it refreshes every ~30s).")
        return False

    # After pairing, connect using the CONNECT port (different from pairing port)
    print(Fore.WHITE + """
  Now go back to the Wireless Debugging screen on your phone.
  The main "IP address & Port" is shown at the top of that page
  (different from the pairing port you just used).
""")
    connect_ip   = prompt("Enter IP address", pair_ip)
    connect_port = prompt("Enter CONNECT PORT shown at top of Wireless Debugging page")

    if not connect_port:
        print_err("No connect port entered.")
        return False

    print_info(f"Connecting to {connect_ip}:{connect_port}...")
    code, out, err = run_adb(["connect", f"{connect_ip}:{connect_port}"])

    output = (out + err).lower()
    if "connected" in output or "already connected" in output:
        print_ok(f"Connected to {connect_ip}:{connect_port}")
        devices = connected_devices()
        if devices:
            print_ok(f"Active devices: {', '.join(devices)}")
        return True
    else:
        print_err(f"Connection failed: {out or err}")
        return False


# ══════════════════════════════════════════════════════════
# MODE 3 — Different Network / WAN / Internet
# ══════════════════════════════════════════════════════════

def mode_wan():
    """
    Connect to a device over the internet (different Wi-Fi network).

    The phone side needs to expose port 5555 to the internet via:
      Option A — Router port forwarding (port 5555 → phone's LAN IP)
      Option B — SSH reverse tunnel or ngrok tunnel on the phone
    """
    print(Fore.CYAN + "\n" + "─" * 60)
    print(Fore.GREEN + Style.BRIGHT + "  MODE 3 — Different Network / Internet (WAN)")
    print(Fore.CYAN + "─" * 60)

    print(Fore.YELLOW + Style.BRIGHT + "\n  Choose how the phone is exposed to the internet:\n")
    print(Fore.WHITE  + "    [A]  Router port forwarding  (you control the router)")
    print(Fore.WHITE  + "    [B]  ngrok tunnel            (easiest, no router access needed)")
    print(Fore.WHITE  + "    [C]  I already have a public IP:port\n")

    choice = prompt("Choose method (A / B / C)", "C").upper()

    if choice == "A":
        _wan_guide_port_forward()
    elif choice == "B":
        _wan_guide_ngrok()

    # In all cases, ask for the final public IP:port to connect
    print(Fore.WHITE + "\n  Enter the PUBLIC IP and PORT where ADB is reachable:")
    public_ip   = prompt("Public IP / hostname (e.g. 203.0.113.45 or abc.ngrok.io)")
    public_port = prompt("Public port (e.g. 5555 or ngrok port)")

    if not public_ip or not public_port:
        print_err("Incomplete details. Returning to menu.")
        return False

    print_info(f"Probing {public_ip}:{public_port}...")
    if not is_ip_reachable(public_ip, int(public_port), timeout=5.0):
        print_err(f"Cannot reach {public_ip}:{public_port}.")
        print_info("Check: Is the port forwarding / tunnel active? Is the phone's ADB running?")
        retry = prompt("Try connecting anyway? (y/n)", "y").lower()
        if retry != "y":
            return False

    print_info(f"Connecting via ADB to {public_ip}:{public_port}...")
    for attempt in range(1, MAX_RETRY + 1):
        code, out, err = run_adb(["connect", f"{public_ip}:{public_port}"], timeout=15)
        output = (out + err).lower()
        if "connected" in output or "already connected" in output:
            print_ok(f"Connected to {public_ip}:{public_port}")
            devices = connected_devices()
            if devices:
                print_ok(f"Active devices: {', '.join(devices)}")
            return True
        else:
            print_err(f"Attempt {attempt}/{MAX_RETRY} failed: {out or err}")
            if attempt < MAX_RETRY:
                time.sleep(2)

    print_err("All connection attempts failed.")
    return False


def _wan_guide_port_forward():
    print(Fore.CYAN + "\n  ── Router Port Forwarding Guide ──")
    print(Fore.WHITE + """
  On the phone (one-time setup via USB or LAN ADB):
    adb tcpip 5555

  On the phone's router:
    1. Log in to your router admin page  (usually 192.168.1.1)
    2. Find  "Port Forwarding"  or  "Virtual Server"
    3. Add a rule:
         External Port : 5555
         Internal IP   : <phone's LAN IP>
         Internal Port : 5555
         Protocol      : TCP
    4. Save and apply

  Find your public IP:
    Visit  https://api.ipify.org  from the phone's network
""")
    input(Fore.YELLOW + "\n  Press ENTER when done...")


def _wan_guide_ngrok():
    print(Fore.CYAN + "\n  ── ngrok Tunnel Guide ──")
    print(Fore.WHITE + """
  ngrok lets you expose your phone's ADB port without touching the router.
  Run these commands on a PC/terminal on the SAME NETWORK as the phone:

  Step 1 — Install ngrok:
    https://ngrok.com/download  (free account needed)

  Step 2 — Enable ADB TCP on phone (USB or LAN first):
    adb tcpip 5555
    adb connect <phone-LAN-ip>:5555

  Step 3 — Start ngrok tunnel:
    ngrok tcp <phone-LAN-ip>:5555

  Step 4 — ngrok will show a line like:
    Forwarding  tcp://0.tcp.ngrok.io:12345  →  ...
    Use   0.tcp.ngrok.io   as Public IP
    Use   12345            as Public Port
""")
    input(Fore.YELLOW + "\n  Press ENTER when done...")


# ══════════════════════════════════════════════════════════
# Main Menu
# ══════════════════════════════════════════════════════════

def main_menu():
    banner()

    print(Fore.WHITE + "  Checking ADB installation...\n")
    if not check_adb_installed():
        sys.exit(1)

    adb_kill_restart_server()

    # Check if already connected
    existing = connected_devices()
    if existing:
        print_ok(f"Already connected device(s): {', '.join(existing)}")
        go = prompt("Launch Pegasus now with current connection? (y/n)", "y").lower()
        if go == "y":
            launch_main_tool()

    while True:
        print(Fore.CYAN + "\n" + "─" * 60)
        print(Fore.GREEN + Style.BRIGHT + "  SELECT CONNECTION MODE\n")
        print(Fore.WHITE  + "    [1]  Same Network / LAN         (phone & PC on same Wi-Fi)")
        print(Fore.WHITE  + "    [2]  Android 11+ Pairing Code   (zero USB, wireless only)")
        print(Fore.WHITE  + "    [3]  Different Network / WAN    (over the internet)")
        print(Fore.RED    + "    [0]  Exit")
        print(Fore.CYAN   + "─" * 60)

        choice = prompt("Enter mode").strip()

        success = False

        if choice == "1":
            success = mode_lan()
        elif choice == "2":
            success = mode_pair()
        elif choice == "3":
            success = mode_wan()
        elif choice == "0":
            print(Fore.YELLOW + "\n  Goodbye!\n")
            sys.exit(0)
        else:
            print_err("Invalid choice. Enter 1, 2, 3, or 0.")
            continue

        if success:
            print(Fore.CYAN + "\n" + "─" * 60)
            print_ok("Device connected successfully!")
            print(Fore.CYAN + "─" * 60)
            input(Fore.YELLOW + "\n  Press ENTER to launch Pegasus...")
            launch_main_tool()
        else:
            retry = prompt("\n  Try a different mode? (y/n)", "y").lower()
            if retry != "y":
                print(Fore.YELLOW + "\n  Exiting.\n")
                sys.exit(1)


# ══════════════════════════════════════════════════════════
# Entry Point
# ══════════════════════════════════════════════════════════

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n\n  Interrupted. Goodbye!\n")
        sys.exit(0)
