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
    print(f"  {G}[H]{W} Generate HTML report")
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
    elif choice == 'H':
        generate_html_report()
    elif choice == 'D':
        clear_logs()


def generate_html_report():
    csv_file = os.path.join("logs", "vulnerable_targets.csv")
    if not os.path.exists(csv_file):
        print(f"{Y}[*] No scan data found to generate HTML report.{W}")
        return
    try:
        with open(csv_file, "r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    except Exception as e:
        print(f"{R}[-] Error reading CSV: {e}{W}")
        return
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows_html = ""
    for i, row in enumerate(rows, 1):
        domain = row.get("domain", "")
        log = row.get("log_file", "")
        rows_html += f"<tr><td>{i}</td><td class='domain'>{domain}</td><td class='log'><code>{log}</code></td></tr>\n"
    empty = "<tr><td colspan='3' class='empty'>No vulnerable targets recorded.</td></tr>" if not rows else ""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SQL Easy — Scan Report</title>
<style>
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',system-ui,sans-serif;background:#0d1117;color:#c9d1d9;padding:2rem;min-height:100vh}}
  h1{{color:#58a6ff;font-size:1.5rem;margin-bottom:.25rem}}
  .sub{{color:#8b949e;font-size:.875rem;margin-bottom:2rem}}
  .badge{{display:inline-block;background:#1f6feb33;color:#58a6ff;border:1px solid #1f6feb;padding:.15rem .5rem;border-radius:10px;font-size:.75rem;margin-left:.4rem;vertical-align:middle}}
  .cards{{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap}}
  .card{{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:1rem 1.5rem;min-width:140px}}
  .card .n{{font-size:2rem;font-weight:700;color:#3fb950}}
  .card .l{{font-size:.75rem;color:#8b949e;margin-top:.25rem;text-transform:uppercase;letter-spacing:.05em}}
  table{{width:100%;border-collapse:collapse;background:#161b22;border:1px solid #30363d;border-radius:8px;overflow:hidden}}
  th{{background:#21262d;color:#58a6ff;padding:.75rem 1rem;text-align:left;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em;font-weight:600}}
  td{{padding:.7rem 1rem;border-top:1px solid #21262d;font-size:.875rem}}
  tr:hover td{{background:#1c2128}}
  td.domain{{color:#f0f6fc;font-weight:500}}
  code{{background:#0d1117;border:1px solid #30363d;padding:.15rem .4rem;border-radius:4px;font-size:.8rem;font-family:'SF Mono',Consolas,monospace;color:#d2a8ff}}
  .empty{{text-align:center;padding:3rem;color:#8b949e}}
  footer{{margin-top:3rem;padding-top:1rem;border-top:1px solid #21262d;color:#8b949e;font-size:.75rem;display:flex;justify-content:space-between}}
</style></head>
<body>
  <h1>SQL Easy <span class="badge">v1.2.0</span></h1>
  <p class="sub">Scan Report &middot; Generated {timestamp}</p>
  <div class="cards">
    <div class="card"><div class="n">{len(rows)}</div><div class="l">Vulnerable Targets</div></div>
  </div>
  <table>
    <thead><tr><th>#</th><th>Domain</th><th>Log File</th></tr></thead>
    <tbody>{rows_html}{empty}</tbody>
  </table>
  <footer><span>SQL Easy v1.2.0</span><span>sqleasy.orildo.sbs</span></footer>
</body></html>"""
    html_file = os.path.join("logs", "report.html")
    try:
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"{G}[+] HTML report saved to {html_file}{W}")
    except Exception as e:
        print(f"{R}[-] Failed to write HTML report: {e}{W}")


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
