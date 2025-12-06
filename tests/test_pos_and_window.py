# tests/test_pos_and_window.py
import numpy as np
import pytest
from types import SimpleNamespace
from cse583_human_say_monkey_do.data_formatting import (
    get_pos_chunk,
    get_windowed_pos_chunk
)


@pytest.fixture
def fake_hdf():
    """Construct a minimal fake HDF5-like dataset."""
    timestamps = np.linspace(0, 1, 101)
    data = np.random.rand(101, 3)
    return SimpleNamespace(timestamps=timestamps, data=data)


def test_get_pos_chunk_basic(fake_hdf):
    start_times = [0.1, 0.3]
    end_times   = [0.2, 0.4]

    # CHANGED: pass timestamps and data separately, not fake_hdf
    chunks = get_pos_chunk(fake_hdf.timestamps, fake_hdf.data, start_times, end_times)

    assert len(chunks) == 2
    assert isinstance(chunks[0], np.ndarray)


def test_get_pos_chunk_smoke(fake_hdf):
    """
    author: Yi Ding
    reviewer:Yici Chen
    category: smoke test
    """
    # CHANGED
    chunks = get_pos_chunk(fake_hdf.timestamps, fake_hdf.data, [0.2], [0.4])
    assert isinstance(chunks, list)
    assert len(chunks) == 1

    chunk = chunks[0]
    assert chunk.size > 0
    assert chunk.shape[1] == fake_hdf.data.shape[1]


def test_get_pos_chunk_one_shot():
    """
    author: Yi Ding
    reviewer:Yici Chen
    category: one shot test
    """
    timestamps = np.array([0.0, 0.1, 0.2, 0.3, 0.4])
    data = np.arange(10).reshape(5, 2)   # easy-to-check values
    hdf = SimpleNamespace(timestamps=timestamps, data=data)

    start = [0.1]
    end = [0.3]

    # CHANGED
    chunks = get_pos_chunk(hdf.timestamps, hdf.data, start, end)

    expected = data[1:4]
    assert np.array_equal(chunks[0], expected)


def test_get_pos_chunk_mismatched_inputs(fake_hdf):
    """
    author: Yi Ding
    reviewer:Yici Chen
    category: edge test
    """
    with pytest.raises(ValueError, match="start_times and end_times must have the same length"):
        # CHANGED
        get_pos_chunk(fake_hdf.timestamps, fake_hdf.data, [0.1], [0.2, 0.3])


def test_get_pos_chunk_sorting(fake_hdf):
    """
    author: Yi Ding
    reviewer:Yici Chen
    category: pattern test (maybe not quite fit
        because the function is not a simple math representation)
    """
    start_times = [0.8, 0.2]
    end_times   = [0.9, 0.3]

    # CHANGED
    chunks = get_pos_chunk(fake_hdf.timestamps, fake_hdf.data, start_times, end_times)

    # After sorting, the first chunk should correspond to the earlier interval (0.2 → 0.3)
    sorted_start = 0.2
    sorted_end   = 0.3

    start_idx = np.searchsorted(fake_hdf.timestamps, sorted_start, side='left')
    end_idx   = np.searchsorted(fake_hdf.timestamps, sorted_end, side='right')

    expected_chunk = fake_hdf.data[start_idx:end_idx]

    assert np.allclose(chunks[0], expected_chunk)


def test_get_windowed_pos_chunk(fake_hdf):
    """windowed pos chunk must call get_pos_chunk logic correctly."""
    centers = [0.3, 0.6]
    window = [0.05, 0.05]

    # CHANGED: pass kinematics (data) and timestamps separately
    chunks = get_windowed_pos_chunk(fake_hdf.data, fake_hdf.timestamps, centers, window)

    assert len(chunks) == 2
    assert isinstance(chunks[0], np.ndarray)