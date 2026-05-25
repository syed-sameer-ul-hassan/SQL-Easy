import os
import csv
import json
import datetime
from core.utils import G, Y, W, R, C

def show_log_manager():
    log_dir = "logs"
    csv_file = os.path.join(log_dir, "vulnerable_targets.csv")

    if not os.path.exists(csv_file):
        print(f"\n{Y}[*] No previous scan logs found. Starting fresh...{W}")
        return

    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"{R}[-] Error reading logs: {e}{W}")
        return

    if not rows:
        print(f"\n{Y}[*] No previous scan logs found. Starting fresh...{W}")
        return

    print(f"\n{Y} +----------------------------------------------------------+{W}")
    print(f"{Y} |             PREVIOUS SCAN RESULTS                       |{W}")
    print(f"{Y} +----------------------------------------------------------+{W}\n")
    print(f"{C} {'#':<5} {'DOMAIN':<30} LOG FILE{W}")
    print(f"{C} {'='*5} {'='*30} {'='*30}{W}")

    for idx, row in enumerate(rows, 1):
        print(f" {G}{idx:<5}{W}{row['domain']:<30} {Y}{row['log_file']}{W}")

    print(f"\n{C}[?] Log Management Options:{W}")
    print(f"  {G}[V]{W} View a specific log file")
    print(f"  {R}[D]{W} Delete all saved logs")
    print(f"  {Y}[ENTER]{W} Skip and start new scan")
    print(f"\n{C}[>] Selection: {W}", end="", flush=True)

    try:
        choice = input().strip().upper()
    except EOFError:
        return

    if choice == 'V':
        print(f"{C}[>] Enter log number to view: {W}", end="", flush=True)
        try:
            num = int(input().strip()) - 1
            if 0 <= num < len(rows):
                log_path = rows[num]['log_file']
                try:
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    print(f"\n{Y}{'='*60}{W}")
                    print(f"{G}[+] Log File: {log_path}{W}")
                    print(f"{Y}{'='*60}{W}\n")
                    print(content)
                    print(f"{Y}{'='*60}{W}")
                    input(f"\n{C}[>] Press ENTER to continue with new scan...{W}")
                except Exception as e:
                    print(f"{R}[-] Could not read log file: {e}{W}")
            else:
                print(f"{R}[-] Invalid log number.{W}")
        except (ValueError, EOFError):
            print(f"{R}[-] Invalid input.{W}")

    elif choice == 'D':
        try:
            os.remove(csv_file)
            print(f"{G}[+] All previous logs cleared successfully.{W}")
        except Exception as e:
            print(f"{R}[-] Failed to delete logs: {e}{W}")


def clear_logs():
    log_dir = "logs"
    targets = [
        os.path.join(log_dir, "vulnerable_targets.csv"),
        os.path.join(log_dir, "vulnerable_targets.json"),
    ]
    cleared = []
    for f in targets:
        if os.path.exists(f):
            try:
                os.remove(f)
                cleared.append(os.path.basename(f))
            except Exception as e:
                print(f"{R}[-] Failed to remove {f}: {e}{W}")
    if cleared:
        print(f"{G}[+] Cleared: {', '.join(cleared)}{W}")
    else:
        print(f"{Y}[*] No log files found to clear.{W}")


def show_report():
    csv_file = os.path.join("logs", "vulnerable_targets.csv")
    json_file = os.path.join("logs", "vulnerable_targets.json")

    if not os.path.exists(csv_file) and not os.path.exists(json_file):
        print(f"\n{Y}[*] No scan reports found. Run a scan first.{W}")
        return

    print(f"\n{Y} +----------------------------------------------------------+{W}")
    print(f"{Y} |                SCAN REPORT SUMMARY                      |{W}")
    print(f"{Y} +----------------------------------------------------------+{W}\n")

    if os.path.exists(csv_file):
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                rows = list(csv.DictReader(f))
            print(f"{G}[+] Vulnerable Targets ({len(rows)} found):{W}")
            print(f"{C} {'#':<5} {'DOMAIN':<30} LOG FILE{W}")
            print(f"{C} {'='*5} {'='*30} {'='*30}{W}")
            for idx, row in enumerate(rows, 1):
                print(f" {G}{idx:<5}{W}{row['domain']:<30} {Y}{row['log_file']}{W}")
        except Exception as e:
            print(f"{R}[-] Error reading CSV report: {e}{W}")

    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"\n{C}[*] JSON report: {json_file} ({len(data)} record(s)){W}")
        except Exception as e:
            print(f"{R}[-] Error reading JSON report: {e}{W}")

    print(f"\n{C}[?] Export Options:{W}")
    print(f"  {G}[J]{W} Re-export to JSON")
    print(f"  {R}[D]{W} Delete all reports")
    print(f"  {Y}[ENTER]{W} Exit")
    print(f"\n{C}[>] Selection: {W}", end="", flush=True)
    try:
        choice = input().strip().upper()
    except EOFError:
        return
    if choice == 'J':
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                rows = list(csv.DictReader(f))
            _write_json(rows)
        except Exception as e:
            print(f"{R}[-] Export failed: {e}{W}")
    elif choice == 'D':
        clear_logs()


def _write_json(vulnerable_urls):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    json_file = os.path.join(log_dir, "vulnerable_targets.json")
    existing = []
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        except Exception:
            existing = []
    seen = {(e.get('domain'), e.get('log_file')) for e in existing}
    for entry in vulnerable_urls:
        key = (entry.get('domain'), entry.get('log_file'))
        if key not in seen:
            existing.append({
                "domain": entry.get("domain"),
                "log_file": entry.get("log_file"),
                "timestamp": datetime.datetime.now().isoformat()
            })
            seen.add(key)
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2)
    print(f"{G}[+] JSON report saved to {json_file}{W}")


def export_results():
    try:
        sqlmap_out = os.path.expanduser("~/.local/share/sqlmap/output")
        if not os.path.exists(sqlmap_out):
            return
            
        print(f"\n{Y}[*] Parsing SQLMap logs...{W}")
        
        vulnerable_urls = []
        
        for root, dirs, files in os.walk(sqlmap_out):
            if "log" in files:
                log_path = os.path.join(root, "log")
                try:
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        if "Parameter:" in content and "Type:" in content:
                            domain = os.path.basename(root)
                            vulnerable_urls.append({"domain": domain, "log_file": log_path})
                except Exception:
                    continue
                    
        if vulnerable_urls:
            log_dir = "logs"
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            csv_file = os.path.join(log_dir, "vulnerable_targets.csv")
            with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['domain', 'log_file']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for row in vulnerable_urls:
                    writer.writerow(row)
                    
            print(f"{G}[+] Injection summary exported to {csv_file}{W}")
            _write_json(vulnerable_urls)
        else:
            print(f"{Y}[*] No confirmed injections found in this scan.{W}")
    except Exception as e:
        print(f"{R}[-] Error during log parsing and export: {e}{W}")
