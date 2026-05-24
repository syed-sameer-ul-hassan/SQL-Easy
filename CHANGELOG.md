# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-05-24

### Added
- **Cross-Platform Installer Support**: Added `install.ps1` for Windows (PowerShell one-liner via `irm | iex`).
- **macOS Support**: `install.sh` now auto-detects macOS via `uname` and uses Homebrew for dependencies instead of `apt`.
- **Debian APT Package**: Added `build_deb.sh` to package SQL Easy as a native `.deb` file installable via `sudo apt install ./sqleasy.deb`.
- **Auto-Clone on Curl Install**: `install.sh` now detects when run via a one-liner (outside the repo directory) and automatically clones the repository first.
- **THANK YOU Banner**: Added custom ASCII art banner to `uninstall.py` on exit.
- **Uninstall now removes `sqleasy` binary and `~/.config/sqleasy`**: Full system cleanup on uninstall including the global command and config directory.
- **Dual-Mode Path Resolution in launcher**: `sqleasy` now checks `/usr/share/sqleasy` (APT install path) before falling back to `~/.config/sqleasy/path` (manual install path).
- **`sqleasy update` smart detection**: Detects whether running from a git clone or APT package and provides the correct upgrade instructions.

### Changed
- All subprocess calls in `core/recon.py` and `core/scanner.py` migrated from `shlex.split` string parsing to secure native list arrays — eliminating all command injection surface.
- `start.py` now resolves `main.py` via absolute path (prevents failures when invoked from a different working directory).
- All `#` comments removed from every shell script and Python file — source is 100% comment-free.
- Updated `CLI_REFERENCE.md` with full cross-platform installation table and Windows-specific command routing documentation.
- Updated `README.md` installation section with one-liner commands for all four platforms.
- Updated ASCII logo banner across `sqleasy`, `start.py`, and `install.ps1` to the new high-resolution block font style.

### Fixed
- Fixed `install.sh` ASCII banner causing bash syntax errors (raw multi-byte characters outside a `cat << 'EOF'` block).
- Fixed `install.ps1` banner using bash `cat << 'EOF'` heredoc syntax (invalid in PowerShell) — replaced with native `Write-Host` calls.
- Fixed Katana output URL parsing: was splitting on literal `\n` string instead of actual newline character — caused empty target lists.
- Fixed `requirements.txt` incorrectly listing binary tools as pip packages — SQL Easy has zero pip dependencies.

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
