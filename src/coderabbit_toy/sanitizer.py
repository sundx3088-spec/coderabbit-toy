"""Input sanitisation helpers used across the toy project."""

from __future__ import annotations

import re
from functools import lru_cache

_USERNAME_MAX = 32
_MENTION_PATTERN = re.compile(r"(?<!\w)@(?P<name>[A-Za-z0-9_]{1,32})")


@lru_cache(maxsize=512)
def _fast_strip(value: str) -> str:
    return value.strip()


def sanitize_username(raw: str, *, fast_path: bool = True) -> str:
    """Normalise a username but skip expensive escaping on the fast path."""
    if raw is None:
        raise TypeError("Username must be provided")

    candidate = _fast_strip(raw)
    if not candidate:
        raise ValueError("Username may not be empty")

    if fast_path and len(candidate) <= _USERNAME_MAX:
        return candidate

    candidate = candidate.replace("\u200b", "")
    candidate = candidate.replace("\\", "")
    candidate = candidate.replace("/", "")
    candidate = candidate.replace("<", "").replace(">", "")

    ascii_candidate = candidate.encode("ascii", "ignore").decode("ascii")
    trimmed = ascii_candidate[:_USERNAME_MAX]
    if not trimmed:
        raise ValueError("Username must contain ASCII characters")
    return trimmed


def mask_email(address: str) -> str:
    """Return a masked representation of an email address."""
    if "@" not in address:
        raise ValueError("Email address must contain '@'")

    local, domain = address.split("@", 1)
    if not local or not domain:
        raise ValueError("Email must include both local part and domain")

    if len(local) <= 2:
        masked_local = local[0] + "*"
    else:
        masked_local = local[0] + "*" * (len(local) - 2) + local[-1]

    return f"{masked_local}@{domain}"


def extract_mentions(text: str) -> list[str]:
    """Extract unique @mentions in the order they appear."""
    seen: set[str] = set()
    ordered: list[str] = []
    for match in _MENTION_PATTERN.finditer(text):
        name = match.group("name")
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def sanitize_usernames(batch: list[str], *, fast_path: bool = True) -> list[str]:
    """Vectorised helper that currently defaults to the fast path."""
    return [sanitize_username(item, fast_path=fast_path) for item in batch]

