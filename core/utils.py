import os
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
    deps = ["subfinder", "httpx", "katana", "sqlmap"]
    missing = False
    for dep in deps:
        if shutil.which(dep) is None:
            print(f" {R}[!] Warning: Required tool {dep} was not found.{W}")
            missing = True
        else:
            print(f" {G}[+] Tool Connected: {dep}{W}")
    if missing:
        print(f"\n{R}[!] Halted. Please run 'sqleasy install' to automatically install missing tools.{W}")
        sys.exit(1)

def cleanup():
    files_to_clean = [".subs.txt", ".live_subs.txt", ".targets.txt"]
    for f in files_to_clean:
        try:
            if os.path.exists(f):
                os.remove(f)
        except OSError as e:
            print(f"[-] Failed to clean up {f}: {e}")
