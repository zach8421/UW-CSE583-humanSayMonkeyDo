# test get_chunk_spikes

import numpy as np
from CSE583_humanSayMonkeyDo.core import get_chunk_spikes


def test_yici_smoke_get_chunk_spikes():
    """
    author: Yici
    reviewer: AJ
    category: smoke test
    note: This test simply checks that the function runs without errors and returns an object of the expected outer structure.
    """
    
    # Minimal valid input — only 1 unit and 1 chunk
    list_units = [np.array([0.1, 0.3, 0.5])]
    start_times = [0.0]
    end_times = [1.0]

    result = get_chunk_spikes(list_units, start_times, end_times)

    # Smoke test: Should run and return a list
    # Basic structure check
    assert isinstance(result, list)


def test_yici_one_shot_get_chunk_spikes():
    """
    author: Yici
    reviewer: AJ
    category: one-shot test
    note: This test uses a fixed and simple input to check whether the returned spikes match the expected exact values.
    """
    
    # Two units with known spike times
    list_units = [
        np.array([0.1, 0.3, 0.5]),   # Unit 0
        np.array([0.2, 0.4])         # Unit 1
    ]
    start_times = [0.0]
    end_times = [0.35]

    result = get_chunk_spikes(list_units, start_times, end_times)

    # Expected filtered spikes
    expected_unit0 = np.array([0.1, 0.3])
    expected_unit1 = np.array([0.2])

    assert np.array_equal(result[0][0], expected_unit0)
    assert np.array_equal(result[0][1], expected_unit1)


def test_yici_edge_get_chunk_spikes_empty_unit():
    """
    author: Yici
    reviewer: AJ
    category: edge test
    note: This test checks how the function behaves when one of the units contains no spikes at all. The output should still include an empty array for that unit.
    """
    list_units = [
        np.array([]),               # edge case: empty unit
        np.array([0.2, 0.4])
    ]
    start_times = [0.0]
    end_times = [1.0]

    result = get_chunk_spikes(list_units, start_times, end_times)

    # The empty unit stays empty
    assert result[0][0].size == 0

    # The non-empty unit should return all spikes
    assert np.array_equal(result[0][1], np.array([0.2, 0.4]))


def test_yici_pattern_get_chunk_spikes_structure():
    """
    author: Yici
    reviewer: AJ
    category: pattern test
    note: This test checks for consistent structural patterns in the output when multiple chunks and units are involved. It does not require exact numerical matching beyond simple patterns.
    """
    list_units = [
        np.array([0.1, 0.5, 1.0]),
        np.array([0.2, 0.6])
    ]
    start_times = [0.0, 0.5]       # two chunks
    end_times = [0.4, 1.2]

    result = get_chunk_spikes(list_units, start_times, end_times)

    # Check chunk and unit structure
    assert len(result) == 2              
    assert len(result[0]) == 2           
    assert len(result[1]) == 2

    # Spikes in expected time ranges
    assert np.array_equal(result[0][0], np.array([0.1]))
    assert np.array_equal(result[1][0], np.array([0.5, 1.0]))
