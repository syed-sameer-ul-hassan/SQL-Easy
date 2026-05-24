# SQL Easy — CLI Command Reference

---

## Overview

Once installed, the `sqleasy` command is available globally in your terminal from any directory on Linux, macOS, and Windows. You never need to `cd` into the project folder.

---

## One-Line Installation

| Platform | Command |
|---|---|
| **Linux** | `bash -c "$(curl -fsSL https://raw.githubusercontent.com/syed-sameer-ul-hassan/SQL-Easy/main/install.sh)"` |
| **macOS** | `bash -c "$(curl -fsSL https://raw.githubusercontent.com/syed-sameer-ul-hassan/SQL-Easy/main/install.sh)"` |
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
| `sqleasy install` | Install all required backend tools |
| `sqleasy uninstall` | Remove all installed backend tools and config |
| `sqleasy update` | Pull the latest version from GitHub |
| `sqleasy help` | Show help menu |
| `sqleasy -h` | Show help menu (shorthand) |

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
| `--proxy` | — | None | Route all traffic through a proxy |
| `--delay` | — | `0` | Seconds between requests |

### Examples

```bash
sqleasy start
sqleasy start -d example.com
sqleasy start -d example.com -t 50
sqleasy start -d example.com --proxy http://127.0.0.1:8080 --delay 3
sqleasy start -d example.com --proxy socks5://127.0.0.1:9050
```

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

## Command: `sqleasy update`

For **git-cloned** installations — runs `git pull` in the SQL Easy installation directory.

For **APT package** installations — advises upgrading via the package manager.

```bash
sqleasy update
```

---

## How Global Commands Work

**Linux / macOS:**
The `sqleasy` Python script is copied to `/usr/local/bin/sqleasy`. The installation path is saved to `~/.config/sqleasy/path` so `sqleasy` can locate `main.py` regardless of what directory you are in.

```
/usr/local/bin/sqleasy           ← runs when you type 'sqleasy'
        ↓
~/.config/sqleasy/path/main.py   ← the actual tool launches here
```

**Windows:**
A `sqleasy.cmd` wrapper is written to `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps\` which calls `python sqleasy` pointing to the cloned directory.

```
sqleasy.cmd    ← runs when you type 'sqleasy' in PowerShell / CMD
     ↓
%USERPROFILE%\sql-easy\sqleasy   ← the Python launcher executes
```
