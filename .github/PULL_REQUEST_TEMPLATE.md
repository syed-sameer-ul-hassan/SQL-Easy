# Pull Request

> SQL Easy v1.2.0 | Please fill out all sections before requesting review.

---

## Description of Changes

Provide a clear description of what changed, why it was needed, and any relevant context.

<!-- Replace this comment with your description -->

## Related Issue

Fixes # (issue number)

---

## Type of Change

- [ ] Bug fix (non-breaking, fixes a reported issue)
- [ ] New feature (non-breaking, adds functionality)
- [ ] Breaking change (existing functionality changes)
- [ ] Documentation update only
- [ ] Performance improvement
- [ ] Security fix
- [ ] New tool integration (arjun / nuclei / gau / gowitness style)
- [ ] New CLI flag (add to `core/config.py` and `sqleasy` help)
- [ ] Platform support (Termux / Docker / Windows / macOS)

---

## Code Quality Checklist

- [ ] I have read [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] My code uses secure list arrays for all subprocess calls (no `shell=True`)
- [ ] All File I/O operations are wrapped in `try...except` blocks
- [ ] I have not introduced any hardcoded paths, credentials, or secrets
- [ ] My code does not use Unicode box-drawing characters or emoji in terminal output
- [ ] All new CLI flags are added to both `core/config.py`, `main.py`, and the `sqleasy` help menu
- [ ] Termux compatibility verified (no `sudo`, `$PREFIX/bin` paths)
- [ ] Architecture-aware binary URLs used (`amd64` / `arm64` / `arm`)
- [ ] I have tested my changes locally end-to-end without errors

## Documentation Checklist

- [ ] README.md updated if the feature affects user-facing behavior
- [ ] CLI_REFERENCE.md updated if new commands or flags were added
- [ ] CONTRIBUTING.md updated if architecture changed
- [ ] CHANGELOG.md updated with a new entry under `[Unreleased]`
- [ ] `config.yaml.example` updated if new flags have default values

## Security Checklist

- [ ] My change does not introduce command injection vectors
- [ ] Temporary files created by my code are cleaned up on exit
- [ ] No sensitive data (target domains, scan results) is leaked to stdout unnecessarily

---

## Testing

Describe how you tested your changes. Include the domain/environment used (use a safe test target like `testphp.vulnweb.com`).

```
Test command used:
sqleasy start -d ...

Expected output:
...

Actual output:
...
```

## Screenshots / Terminal Logs (if applicable)

If your PR changes terminal output, banner, or menu layout, paste a screenshot or log snippet here.

---

*By submitting this PR you confirm you have only tested on systems you own or have explicit written authorization to test.*
