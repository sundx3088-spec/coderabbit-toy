"""Reporting utilities that exercise review scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean


@dataclass(frozen=True)
class UserSnapshot:
    """Lightweight snapshot used in report generation."""

    username: str
    active: bool
    issues_opened: int
    issues_resolved: int


def build_summary(snapshots: list[UserSnapshot], *, include_inactive: bool = False) -> str:
    """Create a human readable summary for dashboard emails."""
    if not snapshots:
        return "No user data available."

    display = ["Weekly Contributor Summary", "==========================="]

    total_opened = 0
    total_resolved = 0
    active_count = 0

    for snap in snapshots:
        if snap.active:
            active_count += 1
        elif not include_inactive:
            continue

        total_opened += snap.issues_opened
        total_resolved += snap.issues_resolved

        delta = snap.issues_resolved - snap.issues_opened
        status = "↑" if delta > 0 else "→" if delta == 0 else "↓"
        display.append(
            f"- @{snap.username} opened {snap.issues_opened} and resolved {snap.issues_resolved} issues ({status})"
        )

    display.append("")
    display.append(f"Active contributors: {active_count}")
    display.append(f"Issues opened: {total_opened}")
    display.append(f"Issues resolved: {total_resolved}")
    return "\n".join(display)


def calculate_growth(history: list[int]) -> float:
    """Return week-over-week growth expressed as a percentage."""
    if len(history) < 2:
        raise ValueError("At least two data points are required")

    if any(value < 0 for value in history):
        raise ValueError("History cannot contain negative numbers")

    previous, current = history[-2:]
    if previous == 0:
        return 100.0 if current > 0 else 0.0

    return round(((current - previous) / previous) * 100, 2)


def rolling_resolution_ratio(history: list[tuple[int, int]]) -> float:
    """Return the average resolved/opened ratio across a history window."""
    if not history:
        raise ValueError("History cannot be empty")

    ratios = []
    for opened, resolved in history:
        if opened < 0 or resolved < 0:
            raise ValueError("Counts cannot be negative")
        if opened == 0:
            ratios.append(1.0 if resolved > 0 else 0.0)
        else:
            ratios.append(resolved / opened)
    return round(mean(ratios), 3)

