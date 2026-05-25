#!/usr/bin/env python3

import sys
import os
import re
import time

if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

from core.config import parse_args
from core.utils import check_dependencies, cleanup, R, C, G, W, Y
from core.display import print_banner, display_targets
from core.recon import run_recon
from core.scanner import execute_attack
from core.logging import show_log_manager, clear_logs, show_report

DOMAIN_RE = re.compile(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def main():
    try:
        args = parse_args()
    except Exception as e:
        print(f"[-] Configuration parsing failed: {e}")
        sys.exit(1)

    if args.logs or args.clear or args.report:
        print_banner()
        if args.logs:
            show_log_manager()
        elif args.clear:
            clear_logs()
            cleanup()
            print(f"\n{G}[+] All logs and temp files wiped clean.{W}")
        elif args.report:
            show_report()
        sys.exit(0)

    try:
        scan_start = time.time()
        print_banner()
        check_dependencies()
        
        domain = args.domain
        if not domain:
            print(f"\n{C}[+] Enter Domain Name (e.g., website.com): {W}", end="", flush=True)
            domain = input().strip()
            if not domain:
                print(f"{R}[-] Domain entry cannot be blank.{W}")
                sys.exit(1)

        if not DOMAIN_RE.match(domain):
            print(f"{R}[-] Invalid domain format: '{domain}'. Use a valid domain (e.g., example.com).{W}")
            sys.exit(1)

        show_log_manager()

        run_recon(domain, args)
        
        target_list = display_targets()
        if target_list:
            execute_attack(target_list, args)
        
        cleanup()
        elapsed = time.time() - scan_start
        mins, secs = divmod(int(elapsed), 60)
        print(f"\n{G}[+] SQL Easy scan pipeline completed safely.{W}")
        print(f"{C}[*] Total scan time: {G}{mins}m {secs}s{W}")
        
    except KeyboardInterrupt:
        print(f"\n\n{R}[!] Process closed by user keyboard shortcut.{W}")
        cleanup()
        sys.exit(0)
    except Exception as e:
        print(f"\n\n{R}[!] Unexpected error occurred: {e}{W}")
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()
