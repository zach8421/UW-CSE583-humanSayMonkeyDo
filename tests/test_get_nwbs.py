# tests/test_get_nwbs.py
import pytest
from pathlib import Path

from src.cse583_human_say_monkey_do.load_config import get_data_paths
from src.cse583_human_say_monkey_do.data_loading import get_nwbs


@pytest.fixture
def data_paths():
    """Fixture to load data paths using project config."""
    return get_data_paths()


def test_get_nwbs_returns_list(data_paths):
    """Basic: get_nwbs should return list of Path objects."""
    nwbs = get_nwbs('monkey')
    assert isinstance(nwbs, list)
    assert all(isinstance(p, Path) for p in nwbs)


def test_get_nwbs_max_subjects(data_paths):
    """max_subjects truncates the output correctly."""
    nwbs_all = get_nwbs('monkey')
    if len(nwbs_all) >= 2:
        nwbs_one = get_nwbs('monkey', max_subjects=1)
        assert len(nwbs_one) == 1

def test_get_nwbs_primate_options():
    """
    Edge test to make sure the function throws a ValueError
    when the input primate is not monkey or human.
    """
    with pytest.raises(ValueError, match="primate must be 'monkey' or 'human'"):
        get_nwbs(primate="gorilla")
