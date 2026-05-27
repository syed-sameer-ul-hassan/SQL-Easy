import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from core.recon import is_injectable_url, prioritize_urls


def test_static_css_rejected():
    assert is_injectable_url("https://example.com/style.css?v=1") is False


def test_static_js_rejected():
    assert is_injectable_url("https://example.com/app.js") is False


def test_static_image_rejected():
    assert is_injectable_url("https://example.com/logo.png") is False


def test_injectable_url_accepted():
    assert is_injectable_url("https://example.com/page?id=1") is True


def test_mixed_params_accepted():
    assert is_injectable_url("https://example.com/view?id=5&v=abc") is True


def test_cache_only_params_rejected():
    assert is_injectable_url("https://example.com/page?_=12345") is False
    assert is_injectable_url("https://example.com/page?v=1&cb=2") is False


def test_prioritize_high_prob_first():
    urls = [
        "https://example.com/page?foo=bar",
        "https://example.com/item?id=1",
        "https://example.com/search?q=test",
    ]
    result = prioritize_urls(urls)
    high_prob = [u for u in result if "id=" in u or "q=" in u]
    normal = [u for u in result if "foo=" in u]
    assert result.index(high_prob[0]) < result.index(normal[0])


def test_prioritize_deduplicates():
    urls = ["https://example.com/?id=1"] * 5
    result = prioritize_urls(urls)
    assert len(result) == 1


def test_prioritize_caps_at_50():
    urls = [f"https://example.com/page?id={i}" for i in range(100)]
    result = prioritize_urls(urls)
    assert len(result) <= 50
