import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.scanner import _get_tamper, _TAMPER_POOL


class _Args:
    tamper = None


def test_get_tamper_default_returns_two_scripts():
    args = _Args()
    result = _get_tamper(args)
    parts = result.split(",")
    assert len(parts) == 2


def test_get_tamper_default_uses_pool():
    args = _Args()
    result = _get_tamper(args)
    for part in result.split(","):
        assert part in _TAMPER_POOL


def test_get_tamper_custom_passthrough():
    args = _Args()
    args.tamper = "space2comment,between,equaltolike"
    result = _get_tamper(args)
    assert result == "space2comment,between,equaltolike"


def test_get_tamper_randomness():
    args = _Args()
    results = {_get_tamper(args) for _ in range(20)}
    assert len(results) > 1
