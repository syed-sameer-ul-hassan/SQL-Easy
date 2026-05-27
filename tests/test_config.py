import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.config import parse_args


def test_default_args(monkeypatch):
    monkeypatch.setattr("sys.argv", ["sqleasy"])
    args = parse_args()
    assert args.threads == 10
    assert args.level == 3
    assert args.risk == 2
    assert args.proxy is None
    assert args.tamper is None
    assert args.resume is False
    assert args.html is False
    assert args.target_list is None


def test_domain_flag(monkeypatch):
    monkeypatch.setattr("sys.argv", ["sqleasy", "-d", "example.com"])
    args = parse_args()
    assert args.domain == "example.com"


def test_resume_flag(monkeypatch):
    monkeypatch.setattr("sys.argv", ["sqleasy", "--resume"])
    args = parse_args()
    assert args.resume is True


def test_html_flag(monkeypatch):
    monkeypatch.setattr("sys.argv", ["sqleasy", "--html"])
    args = parse_args()
    assert args.html is True


def test_tamper_flag(monkeypatch):
    monkeypatch.setattr("sys.argv", ["sqleasy", "--tamper", "space2comment,between"])
    args = parse_args()
    assert args.tamper == "space2comment,between"


def test_target_list_flag(monkeypatch):
    monkeypatch.setattr("sys.argv", ["sqleasy", "--target-list", "domains.txt"])
    args = parse_args()
    assert args.target_list == "domains.txt"


def test_config_defaults_applied(monkeypatch):
    monkeypatch.setattr("sys.argv", ["sqleasy"])
    args = parse_args({"threads": "25", "level": "4"})
    assert args.threads == 25
    assert args.level == 4
