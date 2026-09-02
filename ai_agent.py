#!/usr/bin/env python3
"""
PEGASUS PRO — NVIDIA AI Command Assistant
Provides natural language processing to translate user instructions into ADB actions.
Uses NVIDIA NIM API (OpenAI compatible endpoint).
"""

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
DEFAULT_MODEL = "meta/llama-3.1-70b-instruct"

SYSTEM_PROMPT = """You are an intelligent assistant integrated into PEGASUS PRO, an Android device management suite.
Your role is to translate user natural language requests into safe, valid ADB shell commands or PEGASUS actions.

When the user asks you to do something, provide a short explanation followed by the exact ADB command to run.
Format your output as a JSON object with two fields:
{
  "explanation": "Brief explanation of what this action does",
  "command": "adb command here (e.g., 'adb shell getprop ro.build.version.release')"
}

Do not generate commands designed to extract private user credentials, passwords, or bypass lockscreens maliciously.
Only generate standard administrative, monitoring, diagnostics, and testing commands.
"""

def get_api_key() -> str:
    """Retrieve the NVIDIA API key from environment or prompt."""
    key = os.environ.get("NVIDIA_API_KEY", "").strip()
    if not key:
        config_file = os.path.expanduser("~/.pegasus_nvidia_key")
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    key = f.read().strip()
            except Exception:
                pass
    return key

def save_api_key(key: str):
    """Save key locally for future sessions."""
    config_file = os.path.expanduser("~/.pegasus_nvidia_key")
    try:
        with open(config_file, "w") as f:
            f.write(key.strip())
    except Exception:
        pass

def call_nvidia_ai(prompt: str, api_key: str) -> dict:
    """Send prompt to NVIDIA NIM API and return parsed response."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512,
        "response_format": {"type": "json_object"}
    }
    
    req = urllib.request.Request(
        NVIDIA_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            return json.loads(content)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        return {"error": f"HTTP {e.code}: {err_body}"}
    except Exception as e:
        return {"error": str(e)}

def run_ai_interactive():
    """Interactive loop for AI command mode."""
    print("\n" + "=" * 60)
    print("🤖 PEGASUS PRO — NVIDIA AI Assistant")
    print("=" * 60)
    
    api_key = get_api_key()
    if not api_key:
        print("\nGet your free NVIDIA API key at: https://build.nvidia.com")
        api_key = input("Enter your NVIDIA API Key (nvapi-...): ").strip()
        if not api_key:
            print("[!] No API key provided. Exiting AI mode.")
            return
        save_api_key(api_key)
        print("[✓] API key saved.")

    print("\nAsk anything (e.g., 'check battery level', 'take a screenshot', 'list installed apps')")
    print("Type 'exit' or 'back' to return.\n")

    while True:
        try:
            user_input = input("🤖 AI Command ➤ ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "back", "q", "quit"]:
                break
            
            print("Thinking...")
            res = call_nvidia_ai(user_input, api_key)
            
            if "error" in res:
                print(f"[!] AI Error: {res['error']}")
                continue
                
            explanation = res.get("explanation", "")
            cmd = res.get("command", "")
            
            print(f"\n💡 Plan: {explanation}")
            print(f"🔧 Command: {cmd}")
            
            if cmd:
                execute = input("\nExecute this command? (y/n) [y]: ").strip().lower()
                if execute in ["", "y", "yes"]:
                    print("\n--- Output ---")
                    subprocess.run(cmd, shell=True)
                    print("--------------\n")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    run_ai_interactive()
