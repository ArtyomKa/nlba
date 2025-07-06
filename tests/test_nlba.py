import pytest
from unittest.mock import patch, MagicMock
from nlba.nlba import run_nlba, main
from nlba.llm_interface import MockLLMProvider, GeminiLLMProvider, OpenAILLMProvider
from nlba.config_manager import GLOBAL_CONFIG_FILE, LOCAL_CONFIG_FILE, save_config, load_config
import io
from contextlib import redirect_stdout
import re
import os
import yaml
from pathlib import Path
import sys # Added for sys.argv patching



class MockCommandExecutor:
    def execute_command(self, command: str) -> tuple[str, str, int]:
        if command == "ls -l":
            return "mock_ls_output", "", 0
        elif command == "mkdir new_dir":
            return "", "", 0
        elif command == "rm test_file.txt":
            return "", "", 0
        elif command.startswith("echo 'Mock command for:"):
            return "", "", 0
        elif command == "mkdir new_folder":
            return "", "", 0
        else:
            return f"Mock command not recognized: {command}", "", 1

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_list_files_mock_provider(mock_input):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files in current directory", provider="mock", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: list files in current directory" in output
    assert re.search(r"Generated command: \x1b\[\d+m?ls -l\x1b\[0m", output)
    assert "STDOUT:\n\x1b[92mmock_ls_output\x1b[0m" in output
    assert "Exit Code: \x1b[92m0\x1b[0m" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_create_directory_mock_provider(mock_input):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("create directory new_dir", provider="mock", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: create directory new_dir" in output
    assert re.search(r"Generated command: \x1b\[\d+m?mkdir new_dir\x1b\[0m", output)
    assert "Exit Code: \x1b[91m0\x1b[0m" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_remove_file_mock_provider(mock_input):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("remove file test_file.txt", provider="mock", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: remove file test_file.txt" in output
    assert re.search(r"Generated command: \x1b\[\d+m?rm test_file.txt\x1b\[0m", output)
    assert "Exit Code: \x1b[91m0\x1b[0m" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('nlba.llm_interface.GeminiLLMProvider.generate_command', return_value=('ls -l', 'non-destructive'))
@patch('builtins.input', return_value='y')
def test_list_files_gemini_provider(mock_input, mock_gemini_generate_command):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files in current directory", provider="gemini", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: list files in current directory" in output
    assert re.search(r"Generated command: \x1b\[\d+m?ls -l\x1b\[0m", output)
    assert "STDOUT:\n\x1b[92mmock_ls_output\x1b[0m" in output
    assert "Exit Code: \x1b[92m0\x1b[0m" in output
    mock_gemini_generate_command.assert_called_once_with("list files in current directory")

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('nlba.llm_interface.OpenAILLMProvider.generate_command', return_value=('mkdir new_folder', 'destructive'))
@patch('builtins.input', return_value='y')
def test_create_folder_openai_provider(mock_input, mock_openai_generate_command):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("create a new folder called new_folder", provider="openai", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: create a new folder called new_folder" in output
    assert re.search(r"Generated command: \x1b\[\d+m?mkdir new_folder\x1b\[0m", output)
    assert "Exit Code: \x1b[91m0\x1b[0m" in output
    mock_openai_generate_command.assert_called_once_with("create a new folder called new_folder")

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_set_provider_saves_config(mock_input, setup_config_files):
    global_config_file, _ = setup_config_files
    
    # Ensure config file doesn't exist initially
    if global_config_file.exists():
        global_config_file.unlink()
        with patch('sys.argv', ['nlba', '--set-provider', 'gemini']):
            main()

        assert global_config_file.exists()
        with open(global_config_file, 'r') as f:
            config_data = yaml.safe_load(f)
        assert config_data == {'nlba': {'provider': 'gemini'}}

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    @patch('builtins.input', return_value='n')
    def test_run_nlba_cancel_command(mock_input):
        f = io.StringIO()
        with redirect_stdout(f):
            run_nlba("list files in current directory", provider="mock", skip_confirmation=False)
        output = f.getvalue()
        assert "Command execution cancelled." in output
        assert "STDOUT:" not in output

    def test_main_error_on_missing_request_and_no_set_provider():
        with patch('sys.argv', ['nlba']):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 2  # argparse exits with code 2 on error

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    def test_main_invalid_provider(monkeypatch):
        with patch('sys.argv', ['nlba', 'list files', '--provider', 'invalid', '-y']):
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 2  # argparse should catch invalid choice

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    def test_run_nlba_unknown_provider():
        with pytest.raises(ValueError):
            run_nlba("list files", provider="unknown", skip_confirmation=True)

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    @patch('builtins.input', return_value='y')
    def test_run_nlba_destructive_coloring(mock_input):
        class DestructiveMockProvider:
            def generate_command(self, request):
                return ("rm -rf /", "destructive")
        f = io.StringIO()
        with patch('nlba.llm_interface.MockLLMProvider', new=DestructiveMockProvider):
            with redirect_stdout(f):
                run_nlba("delete everything", provider="mock", skip_confirmation=True)
        output = f.getvalue()
        assert "\033[91mrm -rf /\033[0m" in output
        assert "Exit Code: \033[91m0\033[0m" in output or "Exit Code: \033[91m1\033[0m" in output

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    @patch('builtins.input', return_value='y')
    def test_run_nlba_non_destructive_coloring(mock_input):
        class NonDestructiveMockProvider:
            def generate_command(self, request):
                return ("ls -l", "non-destructive")
        f = io.StringIO()
        with patch('nlba.llm_interface.MockLLMProvider', new=NonDestructiveMockProvider):
            with redirect_stdout(f):
                run_nlba("list files", provider="mock", skip_confirmation=True)
        output = f.getvalue()
        assert "\033[92mls -l\033[0m" in output
        assert "Exit Code: \033[92m0\033[0m" in output

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    @patch('builtins.input', return_value='y')
    def test_run_nlba_stderr_output(mock_input):
        class StderrMockExecutor:
            def execute_command(self, command):
                return "", "error occurred", 1
        f = io.StringIO()
        with patch('nlba.nlba.CommandExecutor', new=StderrMockExecutor):
            with redirect_stdout(f):
                run_nlba("cause error", provider="mock", skip_confirmation=True)
        output = f.getvalue()
        assert "STDERR:" in output
        assert "error occurred" in output

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    @patch('builtins.input', return_value='y')
    def test_run_nlba_no_stdout_stderr(mock_input):
        class EmptyMockExecutor:
            def execute_command(self, command):
                return "", "", 0
        f = io.StringIO()
        with patch('nlba.nlba.CommandExecutor', new=EmptyMockExecutor):
            with redirect_stdout(f):
                run_nlba("do nothing", provider="mock", skip_confirmation=True)
        output = f.getvalue()
        assert "STDOUT:" not in output
        assert "STDERR:" not in output
        assert "Exit Code:" in output

    @patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
    @patch('builtins.input', return_value='y')
    def test_run_nlba_skip_confirmation_flag(mock_input):
        f = io.StringIO()
        with redirect_stdout(f):
            run_nlba("list files", provider="mock", skip_confirmation=True)
            output = f.getvalue()
            assert "Execute this command?" not in output
            # Now test via main() with -y flag
            f.truncate(0)
            f.seek(0)
            with patch('sys.argv', ['nlba', 'list files', '-y']):
                main()
            output = f.getvalue()

            assert "Your request: list files" in output
            assert re.search(r"Generated command: \x1b\[\d+m?ls -l\x1b\[0m", output) # MockLLMProvider returns ls -l
            assert "STDOUT:\n\x1b[92mmock_ls_output\x1b[0m" in output
            assert "Exit Code: \x1b[92m0\x1b[0m" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
@patch('nlba.llm_interface.GeminiLLMProvider.generate_command', return_value=('ls -l', 'non-destructive'))
def test_load_local_config_overrides_global(mock_gemini_generate_command, mock_input, setup_config_files):
    global_config_file, local_config_file = setup_config_files
    
    # Set up global config
    global_config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(global_config_file, 'w') as f:
        yaml.dump({'nlba': {'provider': 'mock'}}, f)

    # Set up local config
    local_config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(local_config_file, 'w') as f:
        yaml.dump({'nlba': {'provider': 'gemini'}}, f)

    f = io.StringIO()
    with redirect_stdout(f):
        with patch('sys.argv', ['nlba', 'list files', '-y']):
            main()
    output = f.getvalue()

    assert "Your request: list files" in output
    # Check that GeminiLLMProvider was used (it would generate a different command or classification if mocked)
    # For this test, we'll rely on the mock_ls_output, but the key is that the provider was 'gemini'
    assert re.search(r"Generated command: \x1b\[\d+m?ls -l\x1b\[0m", output)
    assert "STDOUT:\n\x1b[92mmock_ls_output\x1b[0m" in output
    assert "Exit Code: \x1b[92m0\x1b[0m" in output
    mock_gemini_generate_command.assert_called_once_with("list files")


@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_provider_arg_overrides_config(mock_input, setup_config_files):
    global_config_file, _ = setup_config_files
    
    # Set up a global config file
    global_config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(global_config_file, 'w') as f:
        yaml.dump({'nlba': {'provider': 'openai'}}, f)

    f = io.StringIO()
    with redirect_stdout(f):
        with patch('sys.argv', ['nlba', 'list files', '--provider', 'mock', '-y']):
            main()
    output = f.getvalue()

    assert "Your request: list files" in output
    # Check that MockLLMProvider was used (default mock output)
    assert re.search(r"Generated command: \x1b\[\d+m?ls -l\x1b\[0m", output)
    assert "STDOUT:\n\x1b[92mmock_ls_output\x1b[0m" in output
    assert "Exit Code: \x1b[92m0\x1b[0m" in output
