import os
import re
import subprocess
import shlex
import sys
from core.utils import G, C, Y, W, R

def prioritize_urls(urls):
    high_prob_pattern = re.compile(r"(\?|&)(id|file|page|p|view|dir|doc|cat|search)=")
    
    high_priority = []
    normal_priority = []
    
    unique_urls = list(set(urls))
    
    for url in unique_urls:
        if high_prob_pattern.search(url):
            high_priority.append(url)
        else:
            normal_priority.append(url)
            
    return (high_priority + normal_priority)[:30]

def run_recon(domain, args):
    print(f"\n{G}[+] Target Locked: {W}{domain}")
    print(f"{Y}[*] Starting automation funnel...{W}")
    
    print(f" {C}[>] Running Subfinder...{W}")
    cmd_sub = ["subfinder", "-d", domain, "-silent", "-o", ".subs.txt", "-t", str(args.threads)]
    try:
        subprocess.run(cmd_sub, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    except Exception as e:
        print(f" {R}[!] Subfinder execution failed: {e}{W}")
    
    if not os.path.exists(".subs.txt") or os.path.getsize(".subs.txt") == 0:
        try:
            with open(".subs.txt", "w") as f:
                f.write(domain)
        except Exception as e:
            print(f" {R}[!] Failed to write to .subs.txt: {e}{W}")
            sys.exit(1)

    print(f" {C}[>] Running Httpx...{W}")
    cmd_httpx = ["httpx", "-l", ".subs.txt", "-ports", "80,443,8080,8443,8000", "-silent", "-t", str(args.threads), "-o", ".live_subs.txt"]
    if args.proxy:
        cmd_httpx += ["-http-proxy", args.proxy]
    try:
        subprocess.run(cmd_httpx, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    except Exception as e:
        print(f" {R}[!] Httpx execution failed: {e}{W}")
    
    target_file = ".live_subs.txt" if os.path.exists(".live_subs.txt") and os.path.getsize(".live_subs.txt") > 0 else ".subs.txt"

    print(f" {C}[>] Running Katana...{W}")
    cmd_kat = ["katana", "-list", target_file, "-silent", "-jc", "-kf", "all", "-c", str(args.threads)]
    if args.proxy:
        cmd_kat += ["-proxy", args.proxy]
    if args.delay > 0:
        cmd_kat += ["-delay", str(args.delay)]
    
    try:
        output = subprocess.check_output(cmd_kat, stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError:
        output = ""
    except Exception as e:
        print(f" {R}[!] Katana execution failed: {e}{W}")
        output = ""
        
    urls_with_params = [line.strip() for line in output.split('\n') if line.strip() and '=' in line]
    
    sorted_urls = prioritize_urls(urls_with_params)
    
    try:
        with open(".targets.txt", "w") as f:
            for url in sorted_urls:
                f.write(f"{url}\n")
    except Exception as e:
        print(f" {R}[!] Failed to write targets: {e}{W}")
        sys.exit(1)
