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
from core.utils import check_dependencies, cleanup, load_config, R, C, G, W, Y
from core.display import print_banner, display_targets
from core.recon import run_recon
from core.scanner import execute_attack
from core.logging import show_log_manager, clear_logs, show_report, generate_html_report

DOMAIN_RE = re.compile(r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$')

def _load_domains_from_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except Exception as e:
        print(f"{R}[-] Could not read target list '{path}': {e}{W}")
        sys.exit(1)

def _run_single(domain, args):
    if not DOMAIN_RE.match(domain):
        print(f"{R}[-] Skipping invalid domain: '{domain}'{W}")
        return
    run_recon(domain, args)
    target_list = display_targets()
    if target_list:
        execute_attack(target_list, args)

def main():
    cfg = load_config()
    try:
        args = parse_args(cfg if cfg else None)
    except Exception as e:
        print(f"[-] Configuration parsing failed: {e}")
        sys.exit(1)

    if args.config:
        extra = load_config(args.config)
        if extra:
            try:
                args = parse_args(extra)
            except Exception:
                pass

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

        if args.resume:
            if not os.path.exists(".targets.txt"):
                print(f"{R}[-] --resume set but .targets.txt not found. Run a full scan first.{W}")
                sys.exit(1)
            print(f"\n{Y}[*] Resuming from existing .targets.txt...{W}")
            target_list = display_targets()
            if target_list:
                execute_attack(target_list, args)
        elif args.target_list:
            domains = _load_domains_from_file(args.target_list)
            if not domains:
                print(f"{R}[-] No domains found in '{args.target_list}'.{W}")
                sys.exit(1)
            print(f"\n{C}[*] Batch mode: {len(domains)} domain(s) loaded from {args.target_list}{W}")
            show_log_manager()
            for domain in domains:
                print(f"\n{Y}{'='*60}{W}")
                print(f"{C}[>] Scanning: {G}{domain}{W}")
                print(f"{Y}{'='*60}{W}")
                _run_single(domain, args)
        else:
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
            _run_single(domain, args)

        if getattr(args, "html", False):
            generate_html_report()

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
