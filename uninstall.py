#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import threading
import shutil

R  = "\033[0;31m"
G  = "\033[0;32m"
Y  = "\033[0;33m"
C  = "\033[0;36m"
B  = "\033[1m"
D  = "\033[2m"
W  = "\033[0m"

STEP = 0
TOTAL_STEPS = 4

def step_header(title):
    global STEP
    STEP += 1
    print(f"\n{B}{C}+--------------------------------------------------+{W}")
    print(f"{B}{C}|  Step {STEP}/{TOTAL_STEPS}: {title}{W}")
    print(f"{B}{C}+--------------------------------------------------+{W}")

def spinner_task(msg, stop_event):
    frames = ["-", "\\", "|", "/"]
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r  {C}[{frames[i % 4]}]{W}  {msg}")
        sys.stdout.flush()
        time.sleep(0.08)
        i += 1

def run_with_spinner(msg, func):
    stop = threading.Event()
    t = threading.Thread(target=spinner_task, args=(msg, stop))
    t.start()
    try:
        func()
    finally:
        stop.set()
        t.join()
    sys.stdout.write(f"\r  {G}[+]{W}  {msg:<48} {G}[DONE]{W}\n")
    sys.stdout.flush()

def prompt_yes_no(question):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    while True:
        sys.stdout.write(f"{C}[?] {question} [y/n]: {W}")
        sys.stdout.flush()
        choice = input().lower()
        if choice in valid:
            return valid[choice]
        sys.stdout.write(f"{R}[-] Please respond with 'yes' or 'no'.\n{W}")

def main():
    print(f"{R}")
    print("████████ ██   ██  █████  ███    ██ ██   ██     ██    ██  ██████  ██    ██ ")
    print("   ██    ██   ██ ██   ██ ████   ██ ██  ██       ██  ██  ██    ██ ██    ██ ")
    print("   ██    ███████ ███████ ██ ██  ██ █████         ████   ██    ██ ██    ██ ")
    print("   ██    ██   ██ ██   ██ ██  ██ ██ ██  ██         ██    ██    ██ ██    ██ ")
    print("   ██    ██   ██ ██   ██ ██   ████ ██   ██        ██     ██████   ██████  ")
    print(f"{Y}{B}                  [ SQL Easy Uninstaller v1.1.0 ]{W}")
    print(f"{D}                  https://sqleasy.orildo.sbs{W}\n")

    step_header("Confirmation")
    print(f"  {Y}[!]{W}  This will remove all SQL Easy backend tools from your system.")
    print(f"  {Y}[!]{W}  Your scan logs and results will NOT be deleted.")
    print()
    if not prompt_yes_no("Are you sure you want to remove SQL Easy dependencies?"):
        print(f"\n  {Y}[*]{W}  Uninstall cancelled. Nothing was changed.")
        sys.exit(0)

    step_header("Removing Binaries")
    bins = ["subfinder", "httpx", "katana", "sqleasy"]
    for b in bins:
        path = f"/usr/local/bin/{b}"
        def _remove(p=path):
            subprocess.run(["sudo", "rm", "-f", p], check=False)
        run_with_spinner(f"Removing {path}", _remove)

    step_header("Removing Config Directory")
    config_path = os.path.expanduser("~/.config/sqleasy")
    if os.path.exists(config_path):
        def _rmconfig():
            try:
                shutil.rmtree(config_path)
            except Exception as e:
                print(f"\n  {R}[-]{W}  Failed: {e}")
        run_with_spinner("Removing ~/.config/sqleasy", _rmconfig)
    else:
        print(f"  {D}[~]  Config directory not found, skipping.{W}")

    step_header("Optional: Remove SQLMap")
    if prompt_yes_no("Also uninstall SQLMap via APT?"):
        def _rmsqlmap():
            subprocess.run(["sudo", "apt", "remove", "-y", "sqlmap"],
                           check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        run_with_spinner("Removing sqlmap via apt", _rmsqlmap)
    else:
        print(f"  {D}[~]  Keeping SQLMap.{W}")

    print(f"\n{G}+--------------------------------------------------+{W}")
    print(f"{G}|  Uninstall complete. All dependencies removed.   |{W}")
    print(f"{G}+--------------------------------------------------+{W}")
    print(f"\n  {Y}[*]{W}  To delete the tool folder itself, run:")
    print(f"  {C}       cd .. && rm -rf SQL-Easy{W}\n")

if __name__ == "__main__":
    main()
