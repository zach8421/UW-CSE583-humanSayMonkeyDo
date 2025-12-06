# tests/test_spikes_binned.py
import numpy as np
from src.cse583_human_say_monkey_do.data_formatting import get_chunk_spikes_binned


def test_get_chunk_spikes_binned_basic():
    spikes = [
        np.array([0.05, 0.15, 0.25]),
        np.array([0.1])
    ]
    starts = [0.0]
    ends   = [0.3]

    out, meta = get_chunk_spikes_binned(spikes, starts, ends, bin_size=0.1)

    assert out.shape[0] == 1   # n_chunks
    assert out.shape[1] == 2   # n_units
    assert isinstance(meta, dict)
    assert 'bin_size' in meta
