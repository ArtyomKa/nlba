import pytest
from unittest.mock import patch
import yaml
from pathlib import Path

@pytest.fixture
def setup_config_files(tmp_path):
    # Mock Path.home() and Path.cwd() to control config locations
    mock_home = tmp_path / "home_dir"
    mock_home.mkdir()
    mock_config_dir = mock_home / ".config" / "nlba"
    mock_config_dir.mkdir(parents=True)
    mock_global_config_file = mock_config_dir / "config.yaml"

    mock_cwd = tmp_path / "current_dir"
    mock_cwd.mkdir()
    mock_local_config_dir = mock_cwd / ".nlba"
    mock_local_config_dir.mkdir()
    mock_local_config_file = mock_local_config_dir / "config.yaml"

    with (patch('pathlib.Path.home', return_value=mock_home),
         patch('pathlib.Path.cwd', return_value=mock_cwd),
         patch('nlba.config_manager.GLOBAL_CONFIG_FILE', new=mock_global_config_file),
         patch('nlba.config_manager.LOCAL_CONFIG_FILE', new=mock_local_config_file)):
         yield mock_global_config_file, mock_local_config_file

    # Clean up after tests
    import shutil
    if mock_global_config_file.exists():
        mock_global_config_file.unlink()
    if mock_local_config_file.exists():
        mock_local_config_file.unlink()
    if mock_local_config_dir.exists():
        shutil.rmtree(mock_local_config_dir)
    if mock_config_dir.exists():
        shutil.rmtree(mock_config_dir)
    if mock_home.exists():
        shutil.rmtree(mock_home)
    if mock_cwd.exists():
        shutil.rmtree(mock_cwd)
