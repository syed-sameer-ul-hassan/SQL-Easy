# Security Policy

> Version 1.2.0 | Last updated: 2026-05-27

---

## Supported Versions

Only the latest stable release receives active security patches.
Older versions are unsupported and may contain unpatched vulnerabilities.

| Version | Supported | Notes                        |
| ------- | --------- | ---------------------------- |
| 1.2.x   | Yes       | Current stable release       |
| 1.1.x   | No        | Superseded by v1.2.0         |
| 1.0.x   | No        | Superseded by v1.0.0         |


---

## Scope

Security issues we care about in this project include:

- Command injection via unsanitized user input in subprocess calls
- Insecure file permissions on temp files or config files
- Path traversal in log file handling or config reads
- Credential or token leakage in output or log files
- Privilege escalation in the install or uninstall scripts
- Unsafe use of `shell=True` in any subprocess call

Issues that are out of scope:

- Vulnerabilities in SQLMap, Subfinder, Httpx, Katana, or other third-party tools
- Findings from scanning targets without authorization (those are your liability)
- Social engineering or phishing reports

---

## Reporting a Vulnerability

Do not open a public GitHub issue for security vulnerabilities.

**Primary reporting portal:** [bug.orildo.sbs](https://bug.orildo.sbs)

Alternatively use the GitHub Security Advisory feature:
Repository -> Security tab -> Report a vulnerability

### What to include in your report

1. A clear summary of the vulnerability and its impact
2. The affected version and file/function name
3. Step-by-step reproduction instructions
4. Any relevant log output (scrub real target domains before sending)
5. Suggested fix if you have one

---

## Response Timeline

| Stage              | Target time        |
| ------------------ | ------------------ |
| Acknowledgement    | Within 48 hours    |
| Triage + confirm   | Within 5 days      |
| Patch release      | Within 14 days     |
| Public disclosure  | After patch ships  |

We follow coordinated disclosure. We will credit reporters in the release notes unless you request anonymity.

---

## Ethical Use Reminder

SQL Easy is a penetration testing tool. Maintainers are not responsible for misuse.
Always obtain explicit written authorization before scanning any system you do not own.
Unauthorized use may violate computer crime laws in your jurisdiction.
