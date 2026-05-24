import argparse
import sys

def parse_args():
    try:
        parser = argparse.ArgumentParser(description="SQL Easy Automation Framework")
        parser.add_argument("-d", "--domain", type=str, help="Target domain (e.g., website.com)", required=False)
        parser.add_argument("-t", "--threads", type=int, default=10, help="Concurrency threads for recon tools (default: 10)")
        parser.add_argument("--proxy", type=str, help="Proxy routing (e.g., http://127.0.0.1:8080)", required=False)
        parser.add_argument("--delay", type=int, default=0, help="Custom interaction delay in seconds to avoid rate limiting")
        return parser.parse_args()
    except Exception as e:
        print(f"Argument parsing error: {e}")
        sys.exit(1)
