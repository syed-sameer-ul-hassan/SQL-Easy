import sys
import os
import csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.logging import generate_html_report, clear_logs


def test_html_report_no_csv(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    generate_html_report()
    captured = capsys.readouterr()
    assert "No scan data" in captured.out


def test_html_report_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    csv_file = logs_dir / "vulnerable_targets.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["domain", "log_file"])
        writer.writeheader()
        writer.writerow({"domain": "test.com", "log_file": "/tmp/test.log"})
    generate_html_report()
    html_file = logs_dir / "report.html"
    assert html_file.exists()
    content = html_file.read_text()
    assert "test.com" in content
    assert "SQL Easy" in content


def test_html_report_empty_csv(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    csv_file = logs_dir / "vulnerable_targets.csv"
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["domain", "log_file"])
        writer.writeheader()
    generate_html_report()
    assert (logs_dir / "report.html").exists()


def test_clear_logs_removes_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    logs_dir = tmp_path / "logs"
    logs_dir.mkdir()
    (logs_dir / "vulnerable_targets.csv").write_text("data")
    (logs_dir / "vulnerable_targets.json").write_text("[]")
    clear_logs()
    assert not (logs_dir / "vulnerable_targets.csv").exists()
    assert not (logs_dir / "vulnerable_targets.json").exists()


def test_clear_logs_no_files(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "logs").mkdir()
    clear_logs()
    captured = capsys.readouterr()
    assert "No log files" in captured.out
