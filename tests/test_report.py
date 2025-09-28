import pytest

from coderabbit_toy.report import (
    UserSnapshot,
    build_summary,
    calculate_growth,
    rolling_resolution_ratio,
)


def test_build_summary_includes_active_users():
    snapshots = [
        UserSnapshot("dev1", True, 3, 5),
        UserSnapshot("dev2", False, 1, 1),
    ]
    result = build_summary(snapshots)
    assert "dev1" in result
    assert "dev2" not in result
    assert "Active contributors: 1" in result


def test_build_summary_handles_empty():
    assert build_summary([]) == "No user data available."


def test_calculate_growth_basic():
    assert calculate_growth([2, 4]) == 100.0


def test_calculate_growth_zero_previous():
    assert calculate_growth([0, 5]) == 100.0


def test_calculate_growth_requires_two_values():
    with pytest.raises(ValueError):
        calculate_growth([10])


def test_rolling_resolution_ratio_guards():
    with pytest.raises(ValueError):
        rolling_resolution_ratio([])


def test_rolling_resolution_ratio_average():
    assert rolling_resolution_ratio([(3, 3), (5, 2)]) == 0.667

