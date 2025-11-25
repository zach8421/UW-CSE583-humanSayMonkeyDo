# tests/test_get_nwbs.py
import pytest
from pathlib import Path
from src.CSE583_humanSayMonkeyDo.load_config import get_data_paths
from src.CSE583_humanSayMonkeyDo.core import get_nwbs


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
    """primate must be 'monkey' or 'human'."""
    with pytest.raises(AssertionError):
        get_nwbs('dog')
