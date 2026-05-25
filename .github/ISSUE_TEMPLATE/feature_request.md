---
name: Feature Request
about: Suggest a new idea, integration, or improvement for SQL Easy
title: "[FEATURE] "
labels: enhancement
assignees: ''

---

## Is your feature request related to a problem?
A clear and concise description of what the limitation is. 

*Example:*
> I want to run scans through the Tor network, but setting SOCKS5 proxies manually in the CLI via `--proxy socks5://127.0.0.1:9050` every time is tedious and prone to configuration mistakes.

---

## Describe the solution you'd like
A clear and concise description of what you want to happen. If you are suggesting a code change, please specify which files or modules (`core/recon.py`, `core/scanner.py`, etc.) are affected.

*Example:*
> Add a dedicated `--tor` flag to `core/config.py` which automatically configures SOCKS5 proxy routing (`socks5://127.0.0.1:9050`) for all subprocess calls (Httpx, Katana, SQLmap) and performs a quick public IP check before scanning to ensure routing anonymity is active.

---

## Describe alternatives you've considered
A clear and concise description of any alternative solutions, scripts, or existing tools you've considered.

*Example:*
> Manually editing `core/scanner.py` to hardcode the proxy, but that lacks portability and breaks updates.

---

## Additional Context
Add any other context, mockup screenshots, terminal output concepts, or structural diagrams about the feature request here.
