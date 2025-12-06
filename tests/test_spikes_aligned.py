# tests/test_spikes_aligned.py
import numpy as np
from src.cse583_human_say_monkey_do.data_formatting import get_chunk_spikes_aligned


def test_chunk_spikes_aligned_basic():
    spikes = [
        np.array([0.05, 0.15]),
        np.array([0.1])
    ]
    starts = [0.0]
    ends   = [0.2]

    array, mask, meta = get_chunk_spikes_aligned(spikes, starts, ends)

    assert array.shape[0] == 1
    assert array.shape[1] == 2
    assert 'max_spikes' in meta
    assert mask.shape == array.shape
