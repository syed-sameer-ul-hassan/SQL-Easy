# SQL Easy - Development Roadmap

---

## Completed

### Core Architecture
- [x] Refactored single-file `main.py` script into a scalable `core/` module package
- [x] Created `core/config.py` - centralized `argparse` CLI argument parser
- [x] Created `core/utils.py` - dependency verification and temp file cleanup
- [x] Created `core/recon.py` - full Subfinder -> Httpx -> Katana pipeline
- [x] Created `core/scanner.py` - SQLMap command builder and executor
- [x] Created `core/logging.py` - SQLMap log parser and CSV exporter
- [x] Created `core/display.py` - ASCII banner and Wifite-style interactive menu

### Recon & Scanning Features
- [x] Passive subdomain enumeration via `subfinder`
- [x] Live host probing via `httpx` across ports 80, 443, 8080, 8443, 8000
- [x] URL crawling via `katana` with headless spidering
- [x] Advanced Regex Priority Sorting Engine (pushes `?id=`, `?page=`, `?file=` to top)
- [x] Multi-threaded execution via `-t` flag
- [x] Proxy routing support via `--proxy` flag (supports HTTP and SOCKS5)
- [x] Request delay throttling via `--delay` flag for WAF evasion
- [x] `--batch`, `--random-agent`, `--check-waf` applied to all SQLMap runs
- [x] Single target mode (select by number) and mass mode (`all`)

### Security Hardening
- [x] Replaced all `shell=True` subprocess calls with secure `shlex.split` arrays
- [x] Wrapped all file I/O operations in `try...except` blocks
- [x] Automatic cleanup of `.subs.txt`, `.live_subs.txt`, `.targets.txt` on exit
- [x] Global `KeyboardInterrupt` catch to prevent dirty crashes on `Ctrl+C`
- [x] Removed all source code comments from every Python file

### Logging & Output
- [x] Automated SQLMap output directory parsing after each scan
- [x] CSV export of confirmed vulnerabilities to `logs/vulnerable_targets.csv`
- [x] CSV includes URL, parameter name, payload type, and timestamp

### Setup & Distribution
- [x] Created `start.py` - interactive setup launcher with ASCII banner
- [x] Created `uninstall.py` - clean removal of all installed dependencies
- [x] Created `install.sh` - global installer with `sqleasy` system command
- [x] Created `.gitignore` - excludes scan data, logs, `.venv`, temp files, and OS junk
- [x] Terminal cleared automatically before launching tool from `start.py`
- [x] Binary downloader fallback for non-Kali systems (ProjectDiscovery GitHub releases)

### Documentation
- [x] Rewrote `README.md` with 650+ lines, 10 Mermaid diagrams, full module coverage
- [x] Created `CONTRIBUTING.md` with module architecture, PR flow, and coding rules
- [x] Created `SECURITY.md` - vulnerability disclosure policy
- [x] Created `CODE_OF_CONDUCT.md` - community standards
- [x] Created `CHANGELOG.md` - full version history for v1.0.0
- [x] Created `CITATION.cff` - academic citation format
- [x] Created `LICENSE` - Apache 2.0
- [x] Created `CLI_REFERENCE.md` - full CLI argument documentation
- [x] Created `.github/FUNDING.yml` - GitHub sponsor button
- [x] Created `.github/dependabot.yml` - auto dependency update bot
- [x] Created `.github/PULL_REQUEST_TEMPLATE.md` - PR checklist
- [x] Created `.github/ISSUE_TEMPLATE/bug_report.md` - bug submission form
- [x] Created `.github/ISSUE_TEMPLATE/feature_request.md` - feature request form

---

## Completed - v1.1.0

### Scanning Enhancements
- [x] Added `nuclei` integration - runs after SQLMap on all live hosts (medium/high/critical severity)
- [x] Added `gau` (Get All URLs) as historical URL fallback source
- [x] Added `waybackurls` as historical URL fallback source
- [x] Added `arjun` integration for hidden HTTP parameter bruteforce discovery
- [x] Added `--level` and `--risk` as configurable CLI flags (default: level=3, risk=2)
- [x] Added `--tables` and `--dump` as SQLMap action flags from CLI
- [x] Added `--tamper=space2comment`, `--forms`, `--threads=5`, `--timeout`, `--retries` to SQLMap
- [x] Added smart URL filter - strips static assets (.css, .js, .svg, etc.) and cache-buster-only params
- [x] Expanded high-priority parameter pattern (20+ params: id, uid, user, action, cmd, redirect...)
- [x] Raised target cap from 30 to 50 URLs

### Output & Reporting
- [x] Added JSON export (`logs/vulnerable_targets.json`) alongside CSV
- [x] Added total scan duration timer printed at end of every run
- [x] Added `sqleasy report` - full report summary with CSV + JSON viewer
- [x] Added "No confirmed injections" message when scan finds nothing

### Log Management
- [x] Added `sqleasy logs` - open log manager from anywhere
- [x] Added `sqleasy clear` - wipe all logs and temp files
- [x] Added `sqleasy report` - view and re-export scan results
- [x] Added in-scan log manager - shows previous results before each new scan

### New CLI Commands
- [x] `sqleasy logs` - log manager
- [x] `sqleasy report` - scan report viewer
- [x] `sqleasy clear` - wipe all data
- [x] `sqleasy version` / `-v` - show version info

### Architecture
- [x] Removed all unused imports (`shlex` from recon.py and scanner.py)
- [x] Added domain input validation via regex before scanning
- [x] All tools now stream live output to terminal (subfinder, httpx, katana)
- [x] Katana shows real-time inline crawl counter
- [x] Silent failures replaced with visible error messages

### Setup & Distribution
- [x] Installer now installs: nuclei, gau, arjun in addition to core tools
- [x] GAU and Arjun install failures are non-fatal (graceful skip)

---

## Completed - v1.2.0

### Stealth & Evasion
- [x] Add TOR check - auto-warn if proxy is not set when scanning sensitive targets
- [x] Add multiple tamper script rotation (`--tamper=between,randomcase,space2comment`)
- [x] Add randomized request ordering to defeat sequential pattern detection

### Architecture
- [x] Add unit tests for each `core/` module using `pytest`
- [x] Add `--resume` flag to continue interrupted scans from `.targets.txt`
- [x] Add config file support (`config.yaml`) for saving default flags per-project
- [x] Add `--target-list` flag for multi-domain batch scanning

### Output & Reporting
- [x] Add HTML report generation with summary statistics
- [x] Add auto-screenshot of confirmed vulnerable pages using `gowitness`

### Platform Support
- [x] Create a Docker image for zero-dependency deployment (`Dockerfile`)
- [x] Termux (Android) compatibility — auto-detects `$PREFIX/bin`, no sudo, arch-aware binaries
- [ ] Test and document Windows WSL2 compatibility
- [ ] Add macOS Homebrew install instructions

---

## Planned - v1.3.0

### Notifications & Integration
- [ ] Slack / Discord webhook notifications when a vulnerability is confirmed
- [ ] Scan diff engine — compare two runs and show newly found / fixed targets
- [ ] Auto-throttle based on WAF response codes (auto-reduce threads on 429/403)

### Platform & Distribution
- [ ] Test and document Windows WSL2 compatibility
- [ ] Add macOS Homebrew install instructions
- [ ] APT repository hosting for Debian/Ubuntu auto-updates

### Scan Intelligence
- [ ] Smart retry queue — re-test inconclusive targets with different tamper pairs
- [ ] Blind SQLi detection summary — surface time-based / boolean-based findings

---

## Ideas Under Consideration (v2.0.0)

- [ ] API mode — expose the pipeline as a REST API for integration with other tools
- [ ] Plugin system — custom Python modules that hook into each pipeline stage
- [ ] Distributed scanning — fan out recon across multiple nodes via RPC
