---
name: 🐛 Bug Report
about: Create a detailed bug report to help us improve SQL Easy
title: "[BUG] "
labels: bug
assignees: ''

---

## 📝 Bug Description
A clear and concise description of what the bug is. Please include any background context.

*Example:*
> When launching the crawling phase on subdomains, SQL Easy crashes with a `FileNotFoundError` because Httpx didn't find any live hosts, resulting in an empty `.live_subs.txt` file which Katana then fails to read.

---

## 🕹️ Steps To Reproduce
Steps to reproduce the behavior:
1. Run `sqleasy start -d empty-subdomains-site.com`
2. Let Subfinder complete subdomain enumeration.
3. Observe the crash during Httpx / Katana handoff.

---

## 🎯 Expected Behavior
A clear description of what you expected to happen.

*Example:*
> If no live subdomains are discovered by Httpx, the tool should fallback to testing the main domain directly, or output a graceful warning message and clean up temp files before exiting, rather than crashing with a python traceback.

---

## 💻 Execution Environment
- **OS:** Ubuntu 22.04 LTS / Kali Linux 2024.1
- **Python Version:** 3.10.12
- **SQL Easy Command Used:** `sqleasy start -d example.com -t 20`
- **Dependency Tool Versions:**
  - **Subfinder:** v2.6.6
  - **Httpx:** v1.6.0
  - **Katana:** v1.1.0
  - **SQLmap:** v1.8.2

---

## 📊 Error Logs & Screenshots
If applicable, add terminal logs or screenshot/recording links to help explain the problem.

```text
Traceback (most recent call last):
  File "/home/user/sql-easy/main.py", line 29, in main
    run_recon(domain, args)
  File "/home/user/sql-easy/core/recon.py", line 57, in run_recon
    output = subprocess.check_output(cmd_kat).decode('utf-8')
FileNotFoundError: [Errno 2] No such file or directory: '.live_subs.txt'
```
