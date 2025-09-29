import pytest

from coderabbit_toy import extract_mentions, mask_email, sanitize_username


def test_sanitize_username_strips_and_limits_length():
    result = sanitize_username("   anna-the-builder   ")
    assert result == "anna-the-builder"


def test_sanitize_username_rejects_empty():
    with pytest.raises(ValueError):
        sanitize_username("   ")


def test_sanitize_username_rejects_non_ascii():
    with pytest.raises(ValueError):
        sanitize_username("\u200b\u200b")


def test_mask_email_obscures_middle():
    assert mask_email("astrid@example.com") == "a****d@example.com"


def test_mask_email_handles_short_local():
    assert mask_email("ab@example.com") == "a*@example.com"


def test_extract_mentions_unique_ordered():
    text = "Thanks @alice and @bob, plus @alice again."
    assert extract_mentions(text) == ["alice", "bob"]


def test_sanitize_username_removes_html_markup():
    unsafe = "<script>alert(1)</script>"
    cleaned = sanitize_username(unsafe)
    assert "<" not in cleaned
    assert ">" not in cleaned
    assert "script" in cleaned

