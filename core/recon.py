import os
import re
import subprocess
import sys
import shutil
import urllib.parse
from core.utils import G, C, Y, W, R

STATIC_EXTS = {
    '.css', '.js', '.jpg', '.jpeg', '.png', '.gif', '.svg', '.ico',
    '.woff', '.woff2', '.ttf', '.eot', '.map', '.pdf', '.zip', '.gz',
    '.webp', '.mp4', '.mp3', '.avi', '.mov', '.bmp', '.tiff'
}

CACHE_PARAMS = {
    'v', 'ver', 'version', 'cb', '_', 'hash', 'rev', 'build',
    't', 'ts', 'nocache', 'bust', 'cachekey'
}

def is_injectable_url(url):
    """Return False for static asset URLs or URLs with only cache-buster params."""
    try:
        parsed = urllib.parse.urlparse(url)
        path = parsed.path.lower()
        for ext in STATIC_EXTS:
            if path.endswith(ext):
                return False
        params = urllib.parse.parse_qs(parsed.query)
        if params and all(k.lower() in CACHE_PARAMS for k in params):
            return False
        return True
    except Exception:
        return True

def _stream_run(cmd, output_file=None, show_output=True):
    """Run a command, print output live, and optionally save results to a file."""
    lines = []
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=1,
            universal_newlines=True
        )
        for raw_line in proc.stdout:
            line = raw_line.strip()
            if line:
                if show_output:
                    print(f"   {C}{line}{W}")
                lines.append(line)
        proc.wait()
    except FileNotFoundError:
        print(f" {R}[!] Tool not found: {cmd[0]}{W}")
    except Exception as e:
        print(f" {R}[!] Execution error ({cmd[0]}): {e}{W}")

    if output_file and lines:
        try:
            with open(output_file, 'w') as f:
                f.write('\n'.join(lines) + '\n')
        except Exception as e:
            print(f" {R}[!] Failed to write {output_file}: {e}{W}")

    return lines

def prioritize_urls(urls):
    high_prob_pattern = re.compile(
        r"(\?|&)(id|uid|file|page|p|view|dir|doc|cat|search|query|q|item|product|pid|user|username|name|type|action|cmd|exec|lang|include|path|load|read|fetch|url|src|href|dest|redirect|ref|return)="
    )

    high_priority = []
    normal_priority = []

    unique_urls = list(set(urls))

    for url in unique_urls:
        if not is_injectable_url(url):
            continue
        if high_prob_pattern.search(url):
            high_priority.append(url)
        else:
            normal_priority.append(url)

    return (high_priority + normal_priority)[:50]

def run_recon(domain, args):
    print(f"\n{G}[+] Target Locked: {W}{domain}")
    print(f"{Y}[*] Starting automation funnel...{W}\n")

    # --- Subfinder ---
    print(f" {C}[>] Running Subfinder...{W}")
    cmd_sub = ["subfinder", "-d", domain, "-silent", "-t", str(args.threads)]
    sub_lines = _stream_run(cmd_sub, output_file=".subs.txt", show_output=True)

    if not sub_lines:
        try:
            with open(".subs.txt", "w") as f:
                f.write(domain + '\n')
            sub_lines = [domain]
        except Exception as e:
            print(f" {R}[!] Failed to write to .subs.txt: {e}{W}")
            sys.exit(1)

    print(f" {G}[+] Subfinder: {len(sub_lines)} subdomain(s) found.{W}\n")

    # --- Waybackurls / GAU fallback for extra URL coverage ---
    extra_urls = []
    for tool, cmd in [
        ("waybackurls", ["waybackurls", domain]),
        ("gau",         ["gau", domain, "--threads", str(args.threads)]),
    ]:
        if shutil.which(tool):
            print(f" {C}[>] Running {tool} (historical URL harvest)...{W}")
            extra_urls += _stream_run(cmd, output_file=None, show_output=False)
            print(f" {G}[+] {tool}: {len(extra_urls)} historical URL(s) collected.{W}\n")
            break

    # --- Httpx ---
    print(f" {C}[>] Running Httpx (probing live hosts)...{W}")
    cmd_httpx = ["httpx", "-l", ".subs.txt", "-ports", "80,443,8080,8443,8000", "-silent", "-t", str(args.threads)]
    if args.proxy:
        cmd_httpx += ["-http-proxy", args.proxy]
    httpx_lines = _stream_run(cmd_httpx, output_file=".live_subs.txt", show_output=True)

    if not httpx_lines:
        print(f" {Y}[!] No live hosts found. Falling back to subdomain list.{W}")
    else:
        print(f" {G}[+] Httpx: {len(httpx_lines)} live host(s) confirmed.{W}\n")

    # --- Arjun: hidden parameter bruteforce on live hosts ---
    if shutil.which("arjun") and httpx_lines:
        print(f" {C}[>] Running Arjun (hidden parameter bruteforce)...{W}")
        arjun_found = []
        for target in httpx_lines[:5]:
            try:
                result = subprocess.check_output(
                    ["arjun", "-u", target, "--stable", "-q"],
                    stderr=subprocess.DEVNULL,
                    timeout=90
                ).decode('utf-8', errors='ignore')
                for line in result.split('\n'):
                    line = line.strip()
                    if line and '?' in line and '=' in line:
                        arjun_found.append(line)
            except Exception:
                pass
        if arjun_found:
            extra_urls += arjun_found
            print(f" {G}[+] Arjun: {len(arjun_found)} hidden parameter URL(s) discovered.{W}\n")

    target_file = ".live_subs.txt" if os.path.exists(".live_subs.txt") and os.path.getsize(".live_subs.txt") > 0 else ".subs.txt"

    # --- Katana ---
    print(f" {C}[>] Running Katana (crawling for parameters)...{W}")
    cmd_kat = ["katana", "-list", target_file, "-silent", "-jc", "-kf", "all", "-c", str(args.threads)]
    if args.proxy:
        cmd_kat += ["-proxy", args.proxy]
    if args.delay > 0:
        cmd_kat += ["-delay", str(args.delay)]

    all_urls = []
    try:
        proc = subprocess.Popen(
            cmd_kat,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            bufsize=1,
            universal_newlines=True
        )
        crawl_count = 0
        param_count = 0
        for raw_line in proc.stdout:
            line = raw_line.strip()
            if line:
                crawl_count += 1
                all_urls.append(line)
                if '=' in line:
                    param_count += 1
                print(f"\r   {C}[*] Crawled: {crawl_count} URLs  |  Parameters found: {param_count}{W}   ", end="", flush=True)
        proc.wait()
        print()
    except FileNotFoundError:
        print(f" {R}[!] Tool not found: katana{W}")
    except Exception as e:
        print(f" {R}[!] Katana execution failed: {e}{W}")

    combined_urls = all_urls + extra_urls
    urls_with_params = [url for url in combined_urls if '=' in url]
    sorted_urls = prioritize_urls(urls_with_params)

    injectable_count = len(sorted_urls)
    print(f" {G}[+] Recon complete: {len(urls_with_params)} raw param URL(s) -> {injectable_count} injectable candidate(s) queued.{W}\n")

    try:
        with open(".targets.txt", "w") as f:
            for url in sorted_urls:
                f.write(f"{url}\n")
    except Exception as e:
        print(f" {R}[!] Failed to write targets: {e}{W}")
        sys.exit(1)
