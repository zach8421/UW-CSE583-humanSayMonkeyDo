"""Tests for get_movement_onset_times function"""

from CSE583_humanSayMonkeyDo.core import get_movement_onset_times
import numpy as np
import pandas as pd
from types import SimpleNamespace

def fake_hdf():
    """Construct a minimal fake HDF5-like dataset - containing timestamp and velocity data"""
    timestamps = np.linspace(0, 1, 101)
    velocity_vector = np.vstack([np.linspace(0, 10, 101), np.ones(101)]).T
    return SimpleNamespace(timestamps=timestamps, data=velocity_vector)

def test_princess_correct_structure_get_movement_onset():
    """
    author: Princess
    reviewer: Autumn
    category: pattern test
    note: This test makes sure that velocity dataset has all the correct components
    """
    fake_data = fake_hdf()
    go_cue_time = np.array([0.0])

    # Checks for correct format of velocity data and that they are the same lengths
    assert fake_data.timestamps
    assert fake_data.data
    assert len(fake_data.timestamps) == len(fake_data.data)

    # Check that go_cues are within the time of the experiment
    assert max(go_cue_time) <= fake_data.timestamps[-1]

def test_princess_smoke_get_movement_onset():
    """
    author: Princess
    reviewer: Autumn
    category: Smoke test
    note: evaluates get_movement_onset_times on fake dataset by checking output
    """

    # minimal valid input - HDF5-like dataset and go_cue array
    fake_data = fake_hdf()
    go_cue_time = np.array([0.0])

    movement_time_s, idx = get_movement_onset_times(fake_data, go_cue_time, threshold=5)

    # Should return array of all the movement onset times
    assert isinstance(movement_time_s, np.ndarray)

def test_princess_one_shot_get_movement_onset():
    """
    author: Princess
    reviewer: Autumn
    category: One-shot test
    note: This test checks for a correct number of onsets and that the velocity matches the set threshold value
    """

    fake_data = fake_hdf()
    go_cue_time = np.array([0.0])
    threshold_tests = [1.0, 2.0, 5.0, 8.0]

    for val in threshold_tests:
        movement_time_s, onset_idx = get_movement_onset_times(fake_data, go_cue_time, threshold=val)

    # the number of movement onsets should be the same as the number of go cues
    assert len(onset_idx) == len(go_cue_time)

    # the velocity at the onset is equal to the threshold
    velocity_at_onset = np.linalg.norm(fake_data.data[onset_idx[0]])
    assert velocity_at_onset == threshold_tests


def test_princess_edge_get_movement_onset():
    """
    author: Princess
    reviewer: Autumn
    category: Edge test
    note: This test checks how the function deals with very low velocity thresholds
        The calculation is limited by the size of size of the window and will calculate velocity incorrectly.
    """
    fake_data = fake_hdf()
    go_cue_time = np.array([0.1, 1.0])
    window = [-0.1, 1]
    threshold_tests = [0.1, 0.5, ]

    win_start = abs(int(window[0] / np.median(np.diff(fake_data.timestamps))))
    
    for val in threshold_tests:
        if val <= win_start: 
            raise ValueError(f'threshold must be greater than window offset of {win_start}')
        else:
            movement_time_s, onset_idx = get_movement_onset_times(fake_data, go_cue_time, threshold=val)
    
