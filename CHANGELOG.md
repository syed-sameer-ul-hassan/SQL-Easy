# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-05-25

### Added
- **New CLI commands**: `sqleasy logs`, `sqleasy report`, `sqleasy clear`, `sqleasy version`.
- **Nuclei integration**: Runs broad vuln scan (medium/high/critical) on live hosts after SQLMap.
- **Arjun integration**: Hidden HTTP parameter bruteforce on confirmed live hosts.
- **GAU / Waybackurls integration**: Historical URL harvesting as fallback recon source.
- **`--tables` flag**: SQLMap enumerates database tables in addition to `--dbs`.
- **`--dump` flag**: SQLMap dumps full table contents.
- **`--level` / `--risk` flags**: Configurable SQLMap test depth (default: level=3, risk=2).
- **`--tamper=space2comment`**: Basic WAF evasion on all scans.
- **`--forms`**: SQLMap also tests HTML forms on each target.
- **JSON export**: All results saved to `logs/vulnerable_targets.json` alongside CSV.
- **Scan duration timer**: Total time printed at end of every scan pipeline.
- **Domain validation**: Regex check on domain input before any recon begins.
- **Log manager**: Previous scan results shown before each new scan with view/delete options.
- **Smart URL filtering**: Static assets (.css, .js, .svg, .woff, etc.) and cache-buster-only params excluded from target list.
- **Installer**: `sqleasy install` now also installs Nuclei, GAU, and Arjun.
- **Cross-Platform Installer Support**: Added `install.ps1` for Windows (PowerShell one-liner via `irm | iex`).
- **macOS Support**: `install.sh` now auto-detects macOS via `uname` and uses Homebrew for dependencies instead of `apt`.
- **Debian APT Package**: Added `build_deb.sh` to package SQL Easy as a native `.deb` file.

### Changed
- SQLMap default flags upgraded: `--batch`, `--random-agent`, `--threads=5`, `--timeout=10`, `--retries=2`.
- High-priority parameter pattern expanded to 20+ params (`id, uid, user, action, cmd, exec, redirect`...).
- Target cap raised from 30 to 50 URLs.
- Live output streaming for subfinder and httpx (real-time results instead of silent execution).
- Katana shows inline crawl counter (`Crawled: N URLs | Parameters found: N`).
- Removed obsolete `--check-waf` SQLMap flag (deprecated in SQLMap >= 1.7).
- Removed unused `import shlex` from `core/recon.py` and `core/scanner.py`.

### Fixed
- CSS/JS asset URLs (e.g. `style.css?v=...`) no longer passed to SQLMap as injection targets.
- Subfinder no longer writes to file via `-o` flag; output captured via stdout for live display.
- Httpx no longer writes to file via `-o` flag; output captured via stdout for live display.
- Silent subprocess failures now surface as visible error messages.

---

## [1.0.0] - 2026-05-24

### Added
- Complete `.github` issue templates for bug reporting and feature requests.
- Added comprehensive community standards (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`).
- Multi-threaded execution pipelines via the `-t` CLI argument.
- `httpx` integration to aggressively probe live ports (80, 443, 8080, 8443, 8000) prior to crawling.
- Stealth features: `--proxy` routing support and `--delay` throttling.
- Advanced Regex Prioritization Engine (`core/recon.py`) to sort high-value parameters (`?id=`, `?page=`) to the top of the queue.
- Automated SQLMap log parsing and CSV export engine (`logs/vulnerable_targets.csv`).
- Global `sqleasy` launcher CLI with dynamic install path detection via `~/.config/sqleasy/path`.

### Changed
- Refactored entire codebase from a single `main.py` script to a scalable `core/` module architecture.
- Replaced dangerous `shell=True` subprocess calls with secure argument arrays to prevent OS-level injection vectors.
- Completely rewrote the `README.md` to reflect the new modular architecture, complete with Mermaid diagrams.

### Fixed
- Stabilized file I/O operations (e.g., `.subs.txt` generation) by wrapping them in robust `try...except` blocks to prevent crashes on bad permissions.
- Fixed potential infinite loops and crash vectors by adding global exception catchers in `main.py`.
