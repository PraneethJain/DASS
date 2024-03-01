import pytest
import sys

sys.path.insert(0, "..")
from Code.main import calculate_average, find_highest_scorer


def test_calculate_average():
    assert calculate_average(
        [{"a": [1, 2, 3]}, {"b": [2, 1, 1]}, {"c": [4, 5, 6]}]
    ) == {
        "a": 2.0,
        "b": 4 / 3,
        "c": 5.0,
    }

    assert calculate_average(
        [{"a": [1, 2, 3]}, {"b": [1, 1, 10]}, {"c": [4, 5, 6]}]
    ) == {
        "a": 2.0,
        "b": 4.0,
        "c": 5.0,
    }

    assert calculate_average([{"hello": [90, 120]}, {"bye": [30, 60]}]) == {
        "hello": 105.0,
        "bye": 45.0,
    }


def test_find_highest_scorer():
    assert find_highest_scorer(
        [{"a": [1, 2, 3]}, {"b": [2, 1, 1]}, {"c": [4, 5, 6]}]
    ) == ("c", ["c", "c", "c"])

    assert find_highest_scorer(
        [{"a": [1, 2, 3]}, {"b": [1, 1, 10]}, {"c": [4, 5, 6]}]
    ) == ("c", ["c", "c", "b"])

    assert find_highest_scorer([{"hello": [90, 120]}, {"bye": [30, 60]}]) == (
        "hello",
        ["hello", "hello"],
    )

    with pytest.raises(ValueError):
        find_highest_scorer([])
