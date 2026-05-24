#!/usr/bin/env python3

import sys
from core.config import parse_args
from core.utils import check_dependencies, cleanup, R, C, G, W
from core.display import print_banner, display_targets
from core.recon import run_recon
from core.scanner import execute_attack

def main():
    try:
        args = parse_args()
    except Exception as e:
        print(f"[-] Configuration parsing failed: {e}")
        sys.exit(1)
        
    try:
        print_banner()
        check_dependencies()
        
        domain = args.domain
        if not domain:
            print(f"\n{C}[+] Enter Domain Name (e.g., website.com): {W}", end="")
            domain = input().strip()
            if not domain:
                print(f"{R}[-] Domain entry cannot be blank.{W}")
                sys.exit(1)
                
        run_recon(domain, args)
        
        target_list = display_targets()
        if target_list:
            execute_attack(target_list, args)
        
        cleanup()
        print(f"\n{G}[+] SQL Easy scan pipeline completed safely.{W}")
        
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
