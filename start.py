#!/usr/bin/env python3

import sys
import os
import platform
import subprocess

R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
C = "\033[36m"
W = "\033[0m"

_IS_TERMUX = bool(os.environ.get("TERMUX_VERSION"))
_BIN_DIR = os.environ.get("PREFIX", "/usr/local") + "/bin" if _IS_TERMUX else "/usr/local/bin"
_USE_SUDO = [] if _IS_TERMUX else ["sudo"]
_MACH = platform.machine()
if _MACH in ("x86_64", "AMD64"):
    _ARCH = "amd64"
elif _MACH in ("aarch64", "arm64"):
    _ARCH = "arm64"
elif _MACH.startswith("armv7"):
    _ARCH = "arm"
else:
    _ARCH = "amd64"

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
    print(f"{C}[>] Installing core packages (sqlmap, unzip, wget)...{W}")
    if _IS_TERMUX:
        pkg_cmd = ["pkg", "install", "-y", "sqlmap", "unzip", "wget"]
    else:
        pkg_cmd = ["sudo", "apt", "install", "-y", "sqlmap", "unzip", "wget"]
    subprocess.run(pkg_cmd, check=False)

    print(f"{C}[>] Fetching ProjectDiscovery Binaries (Subfinder, Httpx, Katana, Nuclei)...{W}")
    cmds = [
        ["wget", "-q", f"https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/subfinder_2.6.6_linux_{_ARCH}.zip", "-O", "/tmp/s.zip"],
        ["unzip", "-q", "-o", "/tmp/s.zip", "subfinder", "-d", "/tmp/"],
        ["wget", "-q", f"https://github.com/projectdiscovery/httpx/releases/download/v1.6.0/httpx_1.6.0_linux_{_ARCH}.zip", "-O", "/tmp/h.zip"],
        ["unzip", "-q", "-o", "/tmp/h.zip", "httpx", "-d", "/tmp/"],
        ["wget", "-q", f"https://github.com/projectdiscovery/katana/releases/download/v1.1.0/katana_1.1.0_linux_{_ARCH}.zip", "-O", "/tmp/k.zip"],
        ["unzip", "-q", "-o", "/tmp/k.zip", "katana", "-d", "/tmp/"],
        ["wget", "-q", f"https://github.com/projectdiscovery/nuclei/releases/download/v3.3.9/nuclei_3.3.9_linux_{_ARCH}.zip", "-O", "/tmp/n.zip"],
        ["unzip", "-q", "-o", "/tmp/n.zip", "nuclei", "-d", "/tmp/"],
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError:
            print(f"{R}[-] Error: Failed to fetch binaries. Please check your internet connection.{W}")
            return False
    try:
        for binary in ["subfinder", "httpx", "katana", "nuclei"]:
            subprocess.run(_USE_SUDO + ["mv", f"/tmp/{binary}", _BIN_DIR], check=True)
        subprocess.run(
            _USE_SUDO + ["chmod", "+x"] +
            [f"{_BIN_DIR}/{b}" for b in ["subfinder", "httpx", "katana", "nuclei"]],
            check=True
        )
    except Exception as e:
        print(f"{R}[-] Installation failed during binary move: {e}{W}")
        return False

    print(f"{C}[>] Fetching GAU (Get All URLs)...{W}")
    gau_cmds = [
        ["wget", "-q", f"https://github.com/lc/gau/releases/download/v2.2.4/gau_2.2.4_linux_{_ARCH}.tar.gz", "-O", "/tmp/gau.tar.gz"],
        ["tar", "-xzf", "/tmp/gau.tar.gz", "-C", "/tmp/", "gau"],
    ]
    try:
        for cmd in gau_cmds:
            subprocess.run(cmd, check=True)
        subprocess.run(_USE_SUDO + ["mv", "/tmp/gau", _BIN_DIR], check=True)
        subprocess.run(_USE_SUDO + ["chmod", "+x", f"{_BIN_DIR}/gau"], check=True)
        print(f"{G}[+] GAU installed.{W}")
    except Exception:
        print(f"{Y}[!] GAU install skipped (non-critical).{W}")

    print(f"{C}[>] Installing Arjun (hidden parameter discovery)...{W}")
    try:
        subprocess.run(["pip3", "install", "arjun", "-q"], check=True)
        print(f"{G}[+] Arjun installed.{W}")
    except Exception:
        print(f"{Y}[!] Arjun install skipped (non-critical).{W}")

    print(f"{G}[+] All dependencies successfully installed!{W}\n")
    return True

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
    _pkg_name = "pkg" if _IS_TERMUX else "apt"
    if prompt_yes_no(f"Do you want to automatically install all required backend tools ({_pkg_name})?"):
        install_dependencies()
    else:
        print(f"{Y}[*] Skipping installation. Assuming dependencies are already met.{W}\n")
    start_tool()

if __name__ == "__main__":
    main()
