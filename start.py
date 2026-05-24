#!/usr/bin/env python3

import sys
import os
import subprocess

R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
C = "\033[36m"
W = "\033[0m"

def prompt_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    while True:
        sys.stdout.write(f"{C}[?] {question} [y/n]: {W}")
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(f"{R}[-] Please respond with 'yes' or 'no' (or 'y' or 'n').{W}\n")

def install_dependencies():
    print(f"{Y}[*] Starting automated dependency installation...{W}")
    print(f"{C}[>] Installing SQLMap...{W}")
    subprocess.run(["sudo", "apt", "install", "-y", "sqlmap", "unzip", "wget"], check=False)
    print(f"{C}[>] Fetching ProjectDiscovery Binaries (Subfinder, Httpx, Katana)...{W}")
    cmds = [
        ["wget", "-q", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_amd64.zip", "-O", "/tmp/s.zip"],
        ["unzip", "-q", "-o", "/tmp/s.zip", "subfinder", "-d", "/tmp/"],
        ["wget", "-q", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_amd64.zip", "-O", "/tmp/h.zip"],
        ["unzip", "-q", "-o", "/tmp/h.zip", "httpx", "-d", "/tmp/"],
        ["wget", "-q", "https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_amd64.zip", "-O", "/tmp/k.zip"],
        ["unzip", "-q", "-o", "/tmp/k.zip", "katana", "-d", "/tmp/"],
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"{R}[-] Error: Failed to fetch binaries. Please check your internet connection.{W}")
            return False
    try:
        subprocess.run(["sudo", "mv", "/tmp/subfinder", "/usr/local/bin/"], check=True)
        subprocess.run(["sudo", "mv", "/tmp/httpx", "/usr/local/bin/"], check=True)
        subprocess.run(["sudo", "mv", "/tmp/katana", "/usr/local/bin/"], check=True)
        subprocess.run(["sudo", "chmod", "+x", "/usr/local/bin/subfinder", "/usr/local/bin/httpx", "/usr/local/bin/katana"], check=True)
        print(f"{G}[+] Dependencies successfully installed!{W}\n")
        return True
    except Exception as e:
        print(f"{R}[-] Installation failed during file move operations: {e}{W}")
        return False

def start_tool():
    os.system('clear')
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_path = os.path.join(script_dir, "main.py")
    try:
        subprocess.run([sys.executable, main_path])
    except KeyboardInterrupt:
        print(f"\n{R}[!] Process interrupted.{W}")

def main():
    print(f"{C}")
    print("███████  ██████  ██          ███████  █████  ███████ ██    ██ ")
    print("██      ██    ██ ██          ██      ██   ██ ██       ██  ██  ")
    print("███████ ██    ██ ██          █████   ███████ ███████   ████   ")
    print("     ██ ██ ▄▄ ██ ██          ██      ██   ██      ██    ██    ")
    print("███████  ██████  ███████     ███████ ██   ██ ███████    ██    ")
    print("            ▀▀                                                ")
    print(f"{Y}                  [ SQL Easy Setup & Launcher ]{W}\n")
    if prompt_yes_no("Do you want to automatically install all required backend tools (apt)?"):
        install_dependencies()
    else:
        print(f"{Y}[*] Skipping installation. Assuming dependencies are already met.{W}\n")
    start_tool()

if __name__ == "__main__":
    main()
