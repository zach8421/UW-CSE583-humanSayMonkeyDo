import pytest
from pathlib import Path

# Adjust the import based on your actual structure
from src.cse583_human_say_monkey_do.load_config import load_config, get_config_value, get_data_paths


@pytest.fixture
def config_file_path():
    """Get the path to the actual config.yaml file."""
    # Assuming tests are run from project root
    config_path = Path('config.yaml')
    if not config_path.exists():
        # Try from test directory
        config_path = Path(__file__).parent.parent / 'config.yaml'
    return config_path

def test_load_config_smoke(config_file_path):
    """Smoke test for load_config function.
    author: ajm
    reviewer: 
    category: smoke test"""

    assert config_file_path is not None, "config path returned None"
    assert config_file_path.exists(), f"Config file does not exist at {config_file_path}"

def test_load_config_one_shot(config_file_path):
    """One-shot test for load_config function.
    author: ajm
    reviewer: 
    category: one shot test
    """
    config = load_config(config_file_path)

    assert isinstance(config, dict), "Config is not a dictionary"
    assert 'project_name' in config, "Missing 'project_name' in config"
    assert config['project_name'] == 'humanSayMonkeyDo', "Incorrect 'project_name' value"

def test_load_config_edge_case_empty_file():
    """Edge case test for load_config with an empty file. It should load nothing
    author: ajm
    reviewer: 
    category: edge case test"""
    empty_config_path = Path.cwd() / 'empty_config.yaml'
    empty_config_path.touch()  # Create an empty file
    
    config = load_config(empty_config_path)
    print(config)
    assert config is None, "Config should be None for empty file"
    empty_config_path.unlink()  # Clean up the file


def test_get_data_paths_returns_path_objects_pattern(config_file_path):
    """Test that get_data_paths returns Path objects.
    author: ajm
    reviewer: 
    category: pattern test
    """
    project_root = Path.cwd()
    paths = get_data_paths(project_root=project_root, config_file=config_file_path)
    for key in ['root', 'monkey', 'human']:
        assert key in paths, f"Missing key '{key}' in returned paths"

    assert isinstance(paths['monkey_subjects'], list)
    assert all(isinstance(p, Path) for p in paths['monkey_subjects'])

def test_config_file_exists(config_file_path):
    """Test that config.yaml file exists."""
    assert config_file_path.exists(), f"Config file not found at {config_file_path}"


def test_config_has_required_fields(config_file_path):
    """Test that config.yaml has the required data fields."""
    config = load_config(config_file_path)
    
    assert config is not None, "Config file is empty"
    assert 'data' in config, "Config missing 'data' section"
    assert 'root' in config['data'], "Config missing 'data.root' field"
    assert 'monkey' in config['data'], "Config missing 'data.monkey' field"
    assert 'human' in config['data'], "Config missing 'data.human' field"


def test_load_config(config_file_path):
    """Test that load_config correctly loads the YAML file."""
    config = load_config(config_file_path)
    
    assert isinstance(config, dict)
    assert 'project_name' in config
    assert config['project_name'] == 'humanSayMonkeyDo'
    assert 'data' in config
    assert 'dandi' in config


def test_get_config_value_simple(config_file_path):
    """Test getting a top-level config value."""
    value = get_config_value('project_name', config_file_path)
    assert value == 'humanSayMonkeyDo'


def test_get_config_value_nested(config_file_path):
    """Test getting nested config values using dot notation."""
    monkey_path = get_config_value('data.monkey', config_file_path)
    assert monkey_path == 'data/monkey'
    
    human_path = get_config_value('data.human', config_file_path)
    assert human_path == 'data/human'
    
    root_path = get_config_value('data.root', config_file_path)
    assert root_path == 'data'


def test_get_config_value_dandi(config_file_path):
    """Test getting DANDI configuration values."""
    dataset_id = get_config_value('dandi.dataset_id', config_file_path)
    assert dataset_id == '000688'
    
    version = get_config_value('dandi.version', config_file_path)
    assert version == '0.250122.1735'


def test_get_config_value_monkey_subjects(config_file_path):
    """Test getting monkey subjects list."""
    subjects = get_config_value('data.monkey_subjects', config_file_path)
    assert isinstance(subjects, list)
    assert len(subjects) > 0
    assert 'data/monkey/sub-J' in subjects


def test_get_config_value_invalid_key(config_file_path):
    """Test that invalid keys raise KeyError."""
    with pytest.raises(KeyError):
        get_config_value('nonexistent.key', config_file_path)


def test_get_data_paths_correct_structure(config_file_path):
    """Test that get_data_paths returns correct directory structure."""
    project_root = Path.cwd()
    paths = get_data_paths(project_root=project_root, config_file=config_file_path)
    
    assert paths['root'] == project_root / 'data'
    assert paths['monkey'] == project_root / 'data' / 'monkey'
    assert paths['human'] == project_root / 'data' / 'human'
    assert paths['monkey_subjects'][0] == project_root / 'data' / 'monkey' / 'sub-J'


def test_get_data_paths_absolute_paths(config_file_path):
    """Test that returned paths are absolute when project_root is provided."""
    project_root = Path.cwd()
    paths = get_data_paths(project_root=project_root, config_file=config_file_path)
    
    assert paths['root'].is_absolute()
    assert paths['monkey'].is_absolute()
    assert paths['human'].is_absolute()
    assert all(p.is_absolute() for p in paths['monkey_subjects'])


def test_get_data_paths_default_project_root(config_file_path):
    """Test that get_data_paths works with default project_root."""
    paths = get_data_paths(config_file=config_file_path)
    
    # Should default to config file's parent directory
    expected_root = Path(config_file_path).parent
    assert paths['root'] == expected_root / 'data'


def test_get_data_paths_with_string_project_root(config_file_path):
    """Test that get_data_paths accepts string as project_root."""
    project_root_str = str(Path.cwd())
    paths = get_data_paths(project_root=project_root_str, config_file=config_file_path)
    
    assert paths['monkey'] == Path(project_root_str) / 'data' / 'monkey'


def test_config_yaml_structure(config_file_path):
    """Test that the config has the expected structure."""
    config = load_config(config_file_path)
    
    # Check top-level keys
    assert 'project_name' in config
    assert 'data' in config
    assert 'dandi' in config
    
    # Check data structure
    assert 'root' in config['data']
    assert 'monkey' in config['data']
    assert 'human' in config['data']


def test_data_paths_are_relative_in_config(config_file_path):
    """Test that paths in config are relative (not absolute)."""
    config = load_config(config_file_path)
    
    # Paths should be relative strings, not absolute
    assert not Path(config['data']['root']).is_absolute()
    assert not Path(config['data']['monkey']).is_absolute()
    assert not Path(config['data']['human']).is_absolute()

