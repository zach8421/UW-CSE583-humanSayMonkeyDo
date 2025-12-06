import yaml
from pathlib import Path
import sys

def get_config_path(config_file=Path('config.yaml')):
    """Get the path to the config.yaml file."""
    assert isinstance(config_file, Path), "config_file must be a Path object"

    if not config_file.exists():
        # Try from test directory
        project_root = Path(__file__).parent.parent.parent
        matches = list(project_root.glob("**/" + config_file.name))
        if len(matches)==1:
            config_file = matches[0]
        elif len(matches)>1:
            raise FileNotFoundError(f"Multiple config files found: {matches}")
        elif len(matches)==0:
            raise FileNotFoundError(f"Config file not found at {config_file} or in {project_root}.")
        else:
            raise RuntimeError("Unexpected error locating config file.")

    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found at {config_file}")
    
    return config_file

def load_config(config_file=Path('config.yaml')):
    """Load the config.yaml file."""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def get_config_value(key, config_file=Path('config.yaml')):
    """Get a specific nested value from config using dot notation.
    
    Example: get_config_value('data.monkey')
    """
    config_file = get_config_path(config_file)

    config = load_config(config_file)
    value = config
    for k in key.split('.'):
        value = value[k]
    return value

def get_data_paths(project_root=None, config_file=Path('config.yaml')):
    """Return absolute Path objects for all data directories.
    
    Args:
        project_root: Path to project root. If None, uses config file location.
        config_file: Path to config.yaml file.
    
    Returns:
        dict with Path objects for data directories
    """
    config_file = get_config_path(config_file)

    config = load_config(config_file)
    
    if project_root is None:
        project_root = Path(config_file).parent
    else:
        project_root = Path(project_root)
    
    return {
        'root': project_root / config['data']['root'],
        'monkey': project_root / config['data']['monkey'],
        'human': project_root / config['data']['human'],
        'monkey_subjects': [project_root / subj for subj in config['data']['monkey_subjects']]
    }

# For bash usage - command line interface
if __name__ == '__main__':
    if len(sys.argv) > 1:
        key = sys.argv[1]
        print(get_config_value(key))
    else:
        # Print all data paths as bash variables
        config = load_config()
        print(f"DATA_ROOT={config['data']['root']}")
        print(f"MONKEY_ROOT={config['data']['monkey']}")
        print(f"HUMAN_ROOT={config['data']['human']}")