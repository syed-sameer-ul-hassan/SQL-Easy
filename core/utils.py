import os
import re as _re
import sys
import shutil

R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
C = "\033[36m"
W = "\033[0m"

def check_dependencies():
    print(f"\n{Y}[*] Checking required backend tools...{W}")
    print(f"{C}  +----------------------+----------+{W}")
    required = ["subfinder", "httpx", "katana", "sqlmap"]
    optional = ["nuclei", "arjun", "gau"]
    missing = []
    for dep in required:
        if shutil.which(dep) is None:
            print(f"{C}  | {R}{dep:<20}{W}{C} | {R}MISSING  {C}|{W}")
            missing.append(dep)
        else:
            print(f"{C}  | {G}{dep:<20}{W}{C} | {G}READY    {C}|{W}")
    print(f"{C}  +----------------------+----------+{W}")
    for dep in optional:
        if shutil.which(dep):
            print(f"  {C}[~]{W}  {dep:<18} optional - {G}available{W}")
        else:
            print(f"  {C}[~]{W}  {dep:<18} optional - not installed")
    if missing:
        print(f"\n  {R}[!] Missing: {', '.join(missing)}{W}")
        _hint = "sqleasy install"
        if os.environ.get("TERMUX_VERSION"):
            _hint = "pkg install sqlmap unzip wget && bash install.sh"
        print(f"  {Y}[*] Run '{_hint}' to install them.{W}")
        sys.exit(1)
    print(f"\n  {G}[+] All tools verified. Ready to scan.{W}")

def cleanup():
    files_to_clean = [".subs.txt", ".live_subs.txt", ".targets.txt"]
    for f in files_to_clean:
        try:
            if os.path.exists(f):
                os.remove(f)
        except OSError as e:
            print(f"[-] Failed to clean up {f}: {e}")

def load_config(path=None):
    candidates = [path] if path else ["config.yaml", "sqleasy.yaml"]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            config = {}
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        m = _re.match(r"^([\w-]+):\s*(.+)$", line)
                        if m:
                            config[m.group(1)] = m.group(2).strip()
            except Exception:
                pass
            return config
    return {}
