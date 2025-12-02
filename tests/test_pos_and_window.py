# tests/test_pos_and_window.py
import numpy as np
import pytest
from types import SimpleNamespace
from src.CSE583_humanSayMonkeyDo.core import get_pos_chunk, get_windowed_pos_chunk


@pytest.fixture
def fake_hdf():
    """Construct a minimal fake HDF5-like dataset."""
    timestamps = np.linspace(0, 1, 101)
    data = np.random.rand(101, 3)
    return SimpleNamespace(timestamps=timestamps, data=data)


def test_get_pos_chunk_basic(fake_hdf):
    start_times = [0.1, 0.3]
    end_times   = [0.2, 0.4]
    chunks = get_pos_chunk(fake_hdf, start_times, end_times)

    assert len(chunks) == 2
    assert isinstance(chunks[0], np.ndarray)


def test_get_pos_chunk_mismatched_inputs(fake_hdf):
    """start_times and end_times lengths must match."""
    with pytest.raises(ValueError, match="start_times and end_times must have the same length"):
        get_pos_chunk(fake_hdf, [0.1], [0.2, 0.3])


def test_get_windowed_pos_chunk(fake_hdf):
    """windowed pos chunk must call get_pos_chunk logic correctly."""
    centers = [0.3, 0.6]
    window = [0.05, 0.05]
    chunks = get_windowed_pos_chunk(fake_hdf, centers, window)

    assert len(chunks) == 2
    assert isinstance(chunks[0], np.ndarray)
