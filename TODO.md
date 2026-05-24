# SQL Easy — Development Roadmap

---

## ✅ Completed

### Core Architecture
- [x] Refactored single-file `main.py` script into a scalable `core/` module package
- [x] Created `core/config.py` — centralized `argparse` CLI argument parser
- [x] Created `core/utils.py` — dependency verification and temp file cleanup
- [x] Created `core/recon.py` — full Subfinder → Httpx → Katana pipeline
- [x] Created `core/scanner.py` — SQLMap command builder and executor
- [x] Created `core/logging.py` — SQLMap log parser and CSV exporter
- [x] Created `core/display.py` — ASCII banner and Wifite-style interactive menu

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
- [x] Created `start.py` — interactive setup launcher with ASCII banner
- [x] Created `uninstall.py` — clean removal of all installed dependencies
- [x] Created `install.sh` — global installer with `sqleasy` system command
- [x] Created `.gitignore` — excludes scan data, logs, `.venv`, temp files, and OS junk
- [x] Terminal cleared automatically before launching tool from `start.py`
- [x] Binary downloader fallback for non-Kali systems (ProjectDiscovery GitHub releases)

### Documentation
- [x] Rewrote `README.md` with 650+ lines, 10 Mermaid diagrams, full module coverage
- [x] Created `CONTRIBUTING.md` with module architecture, PR flow, and coding rules
- [x] Created `SECURITY.md` — vulnerability disclosure policy
- [x] Created `CODE_OF_CONDUCT.md` — community standards
- [x] Created `CHANGELOG.md` — full version history for v1.0.0
- [x] Created `CITATION.cff` — academic citation format
- [x] Created `LICENSE` — Apache 2.0
- [x] Created `CLI_REFERENCE.md` — full CLI argument documentation
- [x] Created `.github/FUNDING.yml` — GitHub sponsor button
- [x] Created `.github/dependabot.yml` — auto dependency update bot
- [x] Created `.github/PULL_REQUEST_TEMPLATE.md` — PR checklist
- [x] Created `.github/ISSUE_TEMPLATE/bug_report.md` — bug submission form
- [x] Created `.github/ISSUE_TEMPLATE/feature_request.md` — feature request form

---

## Planned — Next Version (v1.1.0)

### Scanning Enhancements
- [ ] Add `nuclei` integration for broader vulnerability detection beyond SQL injection
- [ ] Add `gau` (Get All URLs) as an alternative to Katana for passive URL collection
- [ ] Add `waybackurls` to collect historical URLs from the Wayback Machine
- [ ] Add `arjun` integration for hidden HTTP parameter discovery
- [ ] Add `--level` and `--risk` as configurable CLI flags (currently hardcoded at 1)
- [ ] Add `--dbs`, `--dump`, `--tables` as optional SQLMap flags from CLI
- [ ] Add `--timeout` flag for HTTP request timeouts

### Output & Reporting
- [ ] Add JSON export option alongside CSV
- [ ] Add HTML report generation with summary statistics
- [ ] Add real-time progress bar using `tqdm` during crawling phase
- [ ] Add color-coded terminal output for confirmed vs potential injections
- [ ] Add total scan duration timer printed at end of run

### Stealth & Evasion
- [ ] Add TOR check — auto-warn if proxy is not set when scanning sensitive targets
- [ ] Add automatic User-Agent rotation pool (not just SQLMap's built-in)
- [ ] Add randomized request ordering to defeat sequential pattern detection

### Architecture
- [ ] Add unit tests for each `core/` module using `pytest`
- [ ] Add `--resume` flag to continue interrupted scans from `.targets.txt`
- [ ] Add plugin system so users can drop in custom scanner modules
- [ ] Add config file support (`config.yaml`) for saving default flags

### Platform Support
- [ ] Test and document Windows WSL2 compatibility
- [ ] Add macOS Homebrew install instructions
- [ ] Create a Docker image for zero-dependency deployment

---

## 💡 Ideas Under Consideration (v2.0.0)

- [ ] Web dashboard UI to visualize scan results in a browser
- [ ] Slack / Discord webhook notifications when a vulnerability is confirmed
- [ ] API mode — expose the pipeline as a REST API for integration with other tools
- [ ] Multi-target file input (`--target-list targets.txt`)
- [ ] Auto-screenshot confirmed vulnerable pages using `gowitness`
