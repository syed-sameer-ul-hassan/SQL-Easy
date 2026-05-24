#!/usr/bin/env python3

import os
import sys
import subprocess

def prompt_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    while True:
        sys.stdout.write(f"\033[36m[?] {question} [y/n]: \033[0m")
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("\033[31m[-] Please respond with 'yes' or 'no' (or 'y' or 'n').\033[0m\n")

def main():
    print("\033[31m")
    print("████████ ██   ██  █████  ███    ██ ██   ██     ██    ██  ██████  ██    ██ ")
    print("   ██    ██   ██ ██   ██ ████   ██ ██  ██       ██  ██  ██    ██ ██    ██ ")
    print("   ██    ███████ ███████ ██ ██  ██ █████         ████   ██    ██ ██    ██ ")
    print("   ██    ██   ██ ██   ██ ██  ██ ██ ██  ██         ██    ██    ██ ██    ██ ")
    print("   ██    ██   ██ ██   ██ ██   ████ ██   ██        ██     ██████   ██████  ")
    print(f"\033[33m                  [ SQL Easy Uninstaller ]\033[0m\n")
    if not prompt_yes_no("Are you sure you want to completely remove SQL Easy dependencies from your system?"):
        print("\033[33m[*] Uninstall cancelled.\033[0m")
        sys.exit(0)
    print("\n\033[33m[*] Starting uninstallation...\033[0m")
    print("\033[36m[>] Removing binaries from /usr/local/bin/...\033[0m")
    bins = ["subfinder", "httpx", "katana", "sqleasy"]
    for b in bins:
        path = f"/usr/local/bin/{b}"
        if os.path.exists(path) or b == "sqleasy":
            subprocess.run(["sudo", "rm", "-f", path], check=False)
            print(f"\033[32m[+] Removed {path}\033[0m")
    config_path = os.path.expanduser("~/.config/sqleasy")
    if os.path.exists(config_path):
        import shutil
        try:
            shutil.rmtree(config_path)
            print("\033[32m[+] Removed config folder ~/.config/sqleasy\033[0m")
        except Exception as e:
            print(f"\033[31m[-] Failed to remove config folder: {e}\033[0m")
    if prompt_yes_no("Do you also want to uninstall SQLMap from your system via APT?"):
        print("\033[36m[>] Removing SQLMap...\033[0m")
        subprocess.run(["sudo", "apt", "remove", "-y", "sqlmap"], check=False)
        print("\033[32m[+] Removed SQLMap\033[0m")
    print("\n\033[32m[+] Dependencies successfully uninstalled!\033[0m")
    print("\033[33m[*] To completely remove the tool itself, step out of this directory and delete it:\033[0m")
    print("\033[36m    cd .. && rm -rf SQL-Easy\033[0m\n")

if __name__ == "__main__":
    main()
