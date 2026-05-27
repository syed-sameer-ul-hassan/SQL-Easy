# SQL Easy - CLI Command Reference (v1.2.0)

---

## Overview

Once installed, the `sqleasy` command is available globally in your terminal from any directory on Linux, macOS, and Windows. You never need to `cd` into the project folder.

---

## One-Line Installation

> **Website:** [sqleasy.orildo.sbs](https://sqleasy.orildo.sbs) | **Bugs:** [bug.orildo.sbs](https://bug.orildo.sbs)
> The installer auto-clones the repository automatically. You do **not** need to `git clone` first.

| Platform | Command |
|---|---|
| **Linux** | `bash -c "$(curl -fsSL https://raw.githubusercontent.com/syed-sameer-ul-hassan/SQL-Easy/main/install.sh)"` |
| **macOS** | `bash -c "$(curl -fsSL https://raw.githubusercontent.com/syed-sameer-ul-hassan/SQL-Easy/main/install.sh)"` |
| **Termux** | `pkg install python wget unzip git && bash -c "$(curl -fsSL https://raw.githubusercontent.com/syed-sameer-ul-hassan/SQL-Easy/main/install.sh)"` |
| **Windows** | `irm https://raw.githubusercontent.com/syed-sameer-ul-hassan/SQL-Easy/main/install.ps1 \| iex` |
| **Debian APT** | `sudo apt install ./sqleasy.deb` |

---

## Getting Help

```bash
sqleasy help
sqleasy -h
```

---

## All Available Commands

| Command | Description |
|---|---|
| `sqleasy start` | Launch SQL Easy interactively |
| `sqleasy start -d <domain>` | Scan a specific domain directly |
| `sqleasy start --target-list <file>` | Batch scan multiple domains from a file |
| `sqleasy start --resume` | Resume from existing `.targets.txt` |
| `sqleasy start --html` | Generate HTML report after scan |
| `sqleasy start --config <file>` | Load default flags from `config.yaml` |
| `sqleasy logs` | Open log manager (view/delete previous results) |
| `sqleasy report` | Show full scan report (CSV + JSON + HTML) |
| `sqleasy clear` | Wipe all scan logs and temp files |
| `sqleasy version` | Show version and pipeline summary |
| `sqleasy install` | Install all required backend tools |
| `sqleasy uninstall` | Remove all installed backend tools and config |
| `sqleasy update` | Pull the latest version from GitHub |
| `sqleasy help` / `-h` | Show help menu |

---

## Command: `sqleasy start`

Launches the full SQL injection pipeline.

```bash
sqleasy start
```

**Options:**

| Option | Short | Default | Description |
|---|---|---|---|
| `--domain` | `-d` | Prompt | Target domain to scan |
| `--threads` | `-t` | `10` | Concurrency threads |
| `--proxy` | - | None | Route all traffic through a proxy |
| `--delay` | - | `0` | Seconds between requests |
| `--level` | - | `3` | SQLMap test level (1-5) |
| `--risk` | - | `2` | SQLMap risk level (1-3) |
| `--tables` | - | off | Enumerate DB tables after finding databases |
| `--dump` | - | off | Dump full table contents (max extraction) |
| `--tamper` | - | auto | SQLMap tamper scripts, comma-separated |
| `--resume` | - | off | Skip recon, resume from `.targets.txt` |
| `--target-list` | - | None | File with one domain per line (batch scan) |
| `--config` | - | None | Path to `config.yaml` with default flag values |
| `--html` | - | off | Generate HTML report after scan |
| `--logs` | - | off | Open log manager without scanning |
| `--report` | - | off | Show report without scanning |
| `--clear` | - | off | Clear all logs without scanning |

### Examples

```bash
sqleasy start
sqleasy start -d example.com
sqleasy start -d example.com -t 50
sqleasy start -d example.com --proxy http://127.0.0.1:8080 --delay 3
sqleasy start -d example.com --proxy socks5://127.0.0.1:9050
sqleasy start -d example.com --level 5 --risk 3
sqleasy start -d example.com --tables
sqleasy start -d example.com --dump
sqleasy start -d example.com --tamper space2comment,between
sqleasy start -d example.com --dump --html
sqleasy start --resume
sqleasy start --target-list domains.txt --html
sqleasy start --config myproject.yaml
```

---

## Command: `sqleasy start --resume`

Skips the recon phase entirely and resumes directly from an existing `.targets.txt` file. Useful if a previous scan was interrupted after recon completed.

```bash
sqleasy start --resume
sqleasy start --resume --dump
```

---

## Command: `sqleasy start --target-list`

Loads a list of domains from a plain-text file (one domain per line) and runs the full recon + attack pipeline for each one sequentially.

```bash
sqleasy start --target-list domains.txt
sqleasy start --target-list domains.txt --html
```

**File format (`domains.txt`):**
```
example.com
target2.org
# comments are ignored
target3.net
```

---

## Command: `sqleasy start --config`

Loads default flag values from a YAML config file. CLI flags always take priority over config file values. If `config.yaml` exists in the working directory it is loaded automatically without specifying `--config`.

```bash
sqleasy start --config myproject.yaml
sqleasy start --config /path/to/project.yaml -d override.com
```

See `config.yaml.example` for the full format.

---

## Command: `sqleasy install`

Installs all required backend tools: `sqlmap`, `subfinder`, `httpx`, `katana`.

```bash
sqleasy install
```

---

## Command: `sqleasy uninstall`

Removes all installed backend tools, the global `sqleasy` binary, and the `~/.config/sqleasy` configuration directory.

```bash
sqleasy uninstall
```

---

## Command: `sqleasy logs`

Opens the log manager. Shows all previous scan results from `logs/vulnerable_targets.csv` and lets you view individual SQLMap log files or delete all saved logs.

```bash
sqleasy logs
```

---

## Command: `sqleasy report`

Displays a full scan report summary including the CSV table and JSON file info. Optionally re-exports results.

```bash
sqleasy report
```

---

## Command: `sqleasy clear`

Wipes all scan logs (`logs/` directory contents) and removes temp files (`.subs.txt`, `.live_subs.txt`, `.targets.txt`).

```bash
sqleasy clear
```

---

## Command: `sqleasy version`

Displays the current version and the full tool pipeline summary.

```bash
sqleasy version
```

---

## Command: `sqleasy update`

For **git-cloned** installations - runs `git pull` in the SQL Easy installation directory.

For **APT package** installations - advises upgrading via the package manager.

```bash
sqleasy update
```

---

## How Global Commands Work

**Linux / macOS:**
The `sqleasy` Python script is copied to `/usr/local/bin/sqleasy`. The installation path is saved to `~/.config/sqleasy/path` so `sqleasy` can locate `main.py` regardless of what directory you are in.

```
/usr/local/bin/sqleasy           <- runs when you type 'sqleasy'
        |
        v
~/.config/sqleasy/path/main.py   <- the actual tool launches here
```

**Windows:**
A `sqleasy.cmd` wrapper is written to `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\` which calls `python sqleasy` pointing to the cloned directory.

```
sqleasy.cmd    <- runs when you type 'sqleasy' in PowerShell / CMD
     |
     v
%USERPROFILE%\sql-easy\sqleasy   <- the Python launcher executes
```
