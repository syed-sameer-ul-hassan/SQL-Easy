import argparse
import sys

def parse_args():
    try:
        parser = argparse.ArgumentParser(description="SQL Easy Automation Framework")
        parser.add_argument("-d", "--domain", type=str, help="Target domain (e.g., website.com)", required=False)
        parser.add_argument("-t", "--threads", type=int, default=10, help="Concurrency threads for recon tools (default: 10)")
        parser.add_argument("--proxy", type=str, help="Proxy routing (e.g., http://127.0.0.1:8080)", required=False)
        parser.add_argument("--delay", type=int, default=0, help="Custom interaction delay in seconds to avoid rate limiting")
        parser.add_argument("--level", type=int, default=3, choices=range(1, 6), metavar="1-5", help="SQLMap test level (default: 3)")
        parser.add_argument("--risk", type=int, default=2, choices=range(1, 4), metavar="1-3", help="SQLMap risk level (default: 2)")
        parser.add_argument("--tables", action="store_true", help="SQLMap: enumerate tables (extends --dbs)")
        parser.add_argument("--dump", action="store_true", help="SQLMap: dump table contents (use responsibly)")
        parser.add_argument("--logs", action="store_true", help="Open log manager without starting a scan")
        parser.add_argument("--clear", action="store_true", help="Clear all saved logs and temp files")
        parser.add_argument("--report", action="store_true", help="Show scan report summary")
        return parser.parse_args()
    except Exception as e:
        print(f"Argument parsing error: {e}")
        sys.exit(1)
