import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.utils import load_config, cleanup


def test_load_config_missing_file():
    result = load_config("nonexistent_config_xyz.yaml")
    assert result == {}


def test_load_config_parses_values(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text("threads: 20\nlevel: 5\nproxy: http://127.0.0.1:8080\n")
    result = load_config(str(cfg))
    assert result["threads"] == "20"
    assert result["level"] == "5"
    assert result["proxy"] == "http://127.0.0.1:8080"


def test_load_config_ignores_comments(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text("# this is a comment\nthreads: 15\n# another comment\ndelay: 2\n")
    result = load_config(str(cfg))
    assert result == {"threads": "15", "delay": "2"}


def test_load_config_empty_file(tmp_path):
    cfg = tmp_path / "config.yaml"
    cfg.write_text("")
    result = load_config(str(cfg))
    assert result == {}


def test_cleanup_removes_temp_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for name in [".subs.txt", ".live_subs.txt", ".targets.txt"]:
        (tmp_path / name).write_text("test")
    cleanup()
    for name in [".subs.txt", ".live_subs.txt", ".targets.txt"]:
        assert not (tmp_path / name).exists()


def test_cleanup_missing_files_no_error(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    cleanup()
