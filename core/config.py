import argparse
import sys

def parse_args(config=None):
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
        parser.add_argument("--tamper", type=str, default=None, metavar="SCRIPTS", help="SQLMap tamper scripts, comma-separated (default: auto-rotated from pool)")
        parser.add_argument("--resume", action="store_true", help="Skip recon and resume from existing .targets.txt")
        parser.add_argument("--target-list", type=str, dest="target_list", metavar="FILE", help="File with one domain per line for batch scanning")
        parser.add_argument("--config", type=str, default=None, metavar="FILE", help="Path to config.yaml with default flag values")
        parser.add_argument("--html", action="store_true", help="Generate HTML report after scan completes")
        parser.add_argument("--logs", action="store_true", help="Open log manager without starting a scan")
        parser.add_argument("--clear", action="store_true", help="Clear all saved logs and temp files")
        parser.add_argument("--report", action="store_true", help="Show scan report summary")
        if config:
            _apply_defaults(parser, config)
        return parser.parse_args()
    except Exception as e:
        print(f"Argument parsing error: {e}")
        sys.exit(1)

def _apply_defaults(parser, config):
    action_map = {a.dest: a for a in parser._actions}
    coerced = {}
    for key, raw in config.items():
        dest = key.replace("-", "_")
        if dest not in action_map:
            continue
        action = action_map[dest]
        try:
            if action.type is not None:
                coerced[dest] = action.type(raw)
            elif action.const is True:
                coerced[dest] = str(raw).lower() in ("true", "1", "yes")
            else:
                coerced[dest] = raw
        except Exception:
            pass
    if coerced:
        parser.set_defaults(**coerced)
