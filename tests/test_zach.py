"""
Test file containing examples of different test types:
- Smoke test
- One-shot test
- Edge test
- Pattern test
"""

import pytest
import numpy as np
from pathlib import Path
from cse583_human_say_monkey_do.core import (
    say_hello,
    get_nwbs,
    get_windowed_pos_chunk
)


# ====================
# SMOKE TEST
# ====================
def test_say_hello_smoke():
    """
    Smoke test: Verify that say_hello runs without crashing.
    This is a simple execution test to ensure the function doesn't fail.

    author: zach8421
    reviewer: Princess
    category: smoke test
    """
    # Just call the function - we're testing that it doesn't crash
    result = say_hello("Test")
    # Basic assertion that something was returned
    assert result is not None


def test_get_nwbs_smoke():
    """
    Smoke test: Verify that get_nwbs runs without crashing.
    Tests basic functionality without deep validation.

    author: zach8421
    reviewer: Princess
    category: smoke test
    """
    # Call with default parameters; main goal is "does not crash"
    result = get_nwbs('monkey')
    assert result is not None


# ====================
# ONE-SHOT TEST
# ====================
def test_say_hello_specific_output():
    """
    One-shot test: Test a specific known input/output pair.
    Verifies exact expected behavior for a single case.

    author: zach8421
    reviewer: Princess
    category: one-shot test
    """
    # Test one specific case with known expected output
    result = say_hello("Alice")
    expected = "Hello, Alice!"
    assert result == expected, f"Expected '{expected}' but got '{result}'"


def test_get_nwbs_max_subjects_one():
    """
    One-shot test: Test get_nwbs with max_subjects=1.
    Verifies that the function respects the limit and returns at most one subject.

    author: zach8421
    reviewer: Princess
    category: one-shot test
    """
    result = get_nwbs('monkey', max_subjects=1)
    # Should never return more than 1
    assert len(result) <= 1, f"Result should have at most 1 item, got {len(result)}"
    # If something is returned, it should be a Path
    if result:
        assert isinstance(result[0], Path), "Result item should be a Path object"


# ====================
# EDGE TEST
# ====================
def test_get_nwbs_invalid_primate():
    """
    Edge test: Test get_nwbs with invalid primate parameter.
    Should raise ValueError for invalid primate types.

    author: zach8421
    reviewer: Princess
    category: edge test
    """
    with pytest.raises(ValueError, match="primate"):
        get_nwbs(primate="gorilla")


def test_get_nwbs_invalid_max_subjects_type():
    """
    Edge test: Test get_nwbs with invalid max_subjects type.
    Should raise TypeError when max_subjects is not an integer.

    author: zach8421
    reviewer: Princess
    category: edge test
    """
    with pytest.raises(TypeError, match="max_subjects"):
        get_nwbs('monkey', max_subjects=1.5)


def test_get_nwbs_zero_max_subjects():
    """
    Edge test: Test get_nwbs with max_subjects=0.
    Should raise ValueError for non-positive max_subjects.

    author: zach8421
    reviewer: Princess
    category: edge test
    """
    with pytest.raises(ValueError, match="max_subjects"):
        get_nwbs('monkey', max_subjects=0)


def test_get_nwbs_negative_max_subjects():
    """
    Edge test: Test get_nwbs with negative max_subjects.
    Should raise ValueError for negative max_subjects.

    author: zach8421
    reviewer: Princess
    category: edge test
    """
    with pytest.raises(ValueError, match="max_subjects"):
        get_nwbs('monkey', max_subjects=-1)


def test_say_hello_empty_string():
    """
    Edge test: Test say_hello with empty string.
    Verifies behavior at the boundary (empty input).

    author: zach8421
    reviewer: Princess
    category: edge test
    """
    result = say_hello("")
    assert result == "Hello, !", "Should handle empty string gracefully"


def test_get_windowed_pos_chunk_invalid_window_size():
    """
    Edge test: Test get_windowed_pos_chunk with invalid window_size.
    Should raise ValueError when window_size doesn't have exactly 2 elements.

    author: zach8421
    reviewer: Princess
    category: edge test
    """
    # Create a mock dataset object
    class MockDataset:
        def __init__(self):
            self.timestamps = np.array([0, 1, 2, 3, 4])
            self.data = np.array([[0], [1], [2], [3], [4]])

    mock_dataset = MockDataset()
    center_times = [1.5]

    # Test with wrong number of window_size elements
    with pytest.raises(ValueError, match="window_size"):
        get_windowed_pos_chunk(mock_dataset, center_times, [1.0])

    with pytest.raises(ValueError, match="window_size"):
        get_windowed_pos_chunk(mock_dataset, center_times, [1.0, 2.0, 3.0])


# ====================
# PATTERN TEST
# ====================
@pytest.mark.parametrize("name,expected", [
    ("World", "Hello, World!"),
    ("Alice", "Hello, Alice!"),
    ("Bob", "Hello, Bob!"),
    ("123", "Hello, 123!"),
    ("", "Hello, !"),
])
def test_say_hello_pattern(name, expected):
    """
    Pattern test: Test say_hello with multiple inputs following the same pattern.
    Verifies that the function consistently produces correct output format.

    author: zach8421
    reviewer: Princess
    category: pattern test
    """
    result = say_hello(name)
    assert result == expected, f"For input '{name}', expected '{expected}' but got '{result}'"


@pytest.mark.parametrize("primate", ["monkey", "human"])
def test_get_nwbs_valid_primates_pattern(primate):
    """
    Pattern test: Test get_nwbs with all valid primate values.
    Ensures consistent behavior across valid inputs.

    author: zach8421
    reviewer: Princess
    category: pattern test
    """
    result = get_nwbs(primate)
    assert isinstance(result, list), f"get_nwbs('{primate}') should return a list"
    assert all(isinstance(p, Path) for p in result), f"All items should be Path objects for primate '{primate}'"


@pytest.mark.parametrize("max_subjects", [1, 2, 5, 10])
def test_get_nwbs_various_max_subjects_pattern(max_subjects):
    """
    Pattern test: Test get_nwbs with various valid max_subjects values.
    Verifies that the limiting behavior works consistently across different limits.

    author: zach8421
    reviewer: Princess
    category: pattern test
    """
    result = get_nwbs('monkey', max_subjects=max_subjects)
    assert len(result) <= max_subjects, \
        f"Result should have at most {max_subjects} items, got {len(result)}"
    assert isinstance(result, list), "Should always return a list"


@pytest.mark.parametrize("invalid_value", [-10, -1, 0])
def test_get_nwbs_invalid_max_subjects_pattern(invalid_value):
    """
    Pattern test: Test get_nwbs with multiple invalid max_subjects values.
    Ensures consistent error handling across similar invalid inputs.

    author: zach8421
    reviewer: Princess
    category: pattern test
    """
    with pytest.raises(ValueError, match="max_subjects"):
        get_nwbs('monkey', max_subjects=invalid_value)
