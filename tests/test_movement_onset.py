# tests/test_movement_onset.py
import numpy as np
from types import SimpleNamespace

from cse583_human_say_monkey_do.analysis import get_movement_onset_times
# CHANGED: removed leading "src." in the import


def test_get_movement_onset_basic():
    timestamps = np.linspace(0, 1, 101)
    velocity = np.vstack([np.linspace(0, 10, 101), np.zeros(101)]).T
    fake_hdf = SimpleNamespace(timestamps=timestamps, data=velocity)

    go_cue_times = np.array([0.0])

    # CHANGED: call with velocity, timestamps, go_cue_times
    times, idx = get_movement_onset_times(
        fake_hdf.data,
        fake_hdf.timestamps,
        go_cue_times,
        threshold=5,
    )

    assert len(times) == 1
    assert not np.isnan(times[0])