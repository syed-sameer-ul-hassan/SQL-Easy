import os
import csv
from core.utils import G, Y, W, R

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
    except Exception as e:
        print(f"{R}[-] Error during log parsing and export: {e}{W}")
