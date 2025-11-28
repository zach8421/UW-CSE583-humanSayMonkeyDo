import os
from pathlib import Path
import pytest

def test_data_download_structure():
    project_root = Path(__file__).parent.parent
    data_dir = project_root / "data"

    # Skip test when running in CI without data directory
    if not data_dir.exists():
        pytest.skip("Skipping data structure test: data directory not available in CI.")

    expected_dirs = [
        data_dir,
        data_dir / "human",
        data_dir / "monkey",
        data_dir / "monkey" / "sub-J",
    ]

    
    for dir_path in expected_dirs:
        assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

    # Check for at least one file in the monkey sub-J directory
    monkey_subj_path = expected_dirs[3]
    files_in_monkey_subj = os.listdir(monkey_subj_path)
    assert len(files_in_monkey_subj) > 0, f"No files found in {monkey_subj_path}."
    # Check for minimum size of files (e.g., at least 1MB total)
    total_size = sum(os.path.getsize(os.path.join(monkey_subj_path, f)) for f in files_in_monkey_subj)
    assert total_size >= 1 * 1024 * 1024, f"Total size of files in {monkey_subj_path} is less than 1MB."

    #TODO: Human data checks can be added when data is available

    print("All data download structure tests passed.")
    return
    
