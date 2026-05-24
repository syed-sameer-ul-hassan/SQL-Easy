import os
import sys
from core.utils import R, G, Y, B, C, W, cleanup

def print_banner():
    print(f"""{C}
  ▄▄▄▄▄▄ .▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
  █      ██      █       █       █       █       █       █
  █  ▄▄▄▄██  ▄▄  █   ▄   █    ▄▄▄█    ▄▄▄█▄▄   ▄▄█    ▄▄▄█
  █  █▄▄▄▄█  █ █ █  █ █  █   █▄▄▄█   █▄▄▄  █   █ █   █▄▄▄ 
  █▄▄▄▄  ██  █▄█ █  █▄█  █    ▄▄▄█    ▄▄▄█ █   █ █    ▄▄▄█
  █      ██      █       █   █   █   █     █   █ █       █
  ▀▀▀▀▀▀▀ ▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀    ▀▀▀▀      ▀▀▀▀  ▀▀▀▀▀▀▀  
                  {Y}[ SQL Easy Automation Framework ]{W}""")

def display_targets():
    if not os.path.exists(".targets.txt") or os.path.getsize(".targets.txt") == 0:
        print(f"\n{R}[-] No input parameters detected on this domain. Try another target.{W}")
        cleanup()
        sys.exit(0)

    try:
        with open(".targets.txt", "r") as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
    except Exception as e:
        print(f"\n{R}[-] Error reading targets file: {e}{W}")
        sys.exit(1)

    print(f"\n{Y} NUM   AVAILABLE PARAMETER TARGETS (WIFITE-STYLE MENU){W}")
    print(f"{C} ---   ------------------------------------------------{W}")
    
    for idx, url in enumerate(urls, 1):
        print(f" {G}{idx:<5}{W}{url}")
    
    return urls
