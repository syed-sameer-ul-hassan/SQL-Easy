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

    count = len(urls)
    print(f"\n{Y}  +------------------------------------------------------------+{W}")
    print(f"{Y}  |  AVAILABLE PARAMETER TARGETS  ({count} found){' '*(26-len(str(count)))}|{W}")
    print(f"{Y}  +------------------------------------------------------------+{W}")
    print(f"\n{C}  {'No.':<5}  Target URL{W}")
    print(f"{C}  {'---':<5}  {'-'*55}{W}")

    for idx, url in enumerate(urls, 1):
        display_url = url if len(url) <= 70 else url[:67] + '...'
        print(f"  {G}{idx:<5}{W}  {display_url}")

    print(f"{C}  {'---':<5}  {'-'*55}{W}\n")
    return urls
