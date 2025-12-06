# tests/test_spikes.py
import numpy as np
from src.cse583_human_say_monkey_do.data_formatting import get_chunk_spikes


def test_get_chunk_spikes_list_format():
    spikes = [np.array([0.1, 0.2, 0.3]), np.array([])]
    starts = [0.0]
    ends   = [0.25]

    out = get_chunk_spikes(spikes, starts, ends, return_format='list')
    assert isinstance(out, list)
    assert isinstance(out[0], list)
    assert isinstance(out[0][0], np.ndarray)


def test_get_chunk_spikes_dict_format():
    spikes = [np.array([0.1, 0.2]), np.array([])]
    starts = [0.0]
    ends   = [0.25]

    out = get_chunk_spikes(spikes, starts, ends, return_format='dict')
    assert 'spikes' in out
    assert 'counts' in out
    assert out['n_units'] == 2


def test_get_chunk_spikes_ragged_format():
    spikes = [np.array([0.1]), np.array([0.15, 0.2])]
    starts = [0.0]
    ends   = [0.3]

    out = get_chunk_spikes(spikes, starts, ends, return_format='ragged')
    assert 'data' in out
    assert 'spike_counts' in out
