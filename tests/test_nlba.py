import pytest
from unittest.mock import patch
from nlba.nlba import run_nlba
from nlba.llm_interface import MockLLMProvider, GeminiLLMProvider, OpenAILLMProvider

# Mock CommandExecutor to prevent actual shell commands during tests
class MockCommandExecutor:
    def execute_command(self, command: str) -> tuple[str, str, int]:
        # Simulate successful execution for testing purposes
        if command == "ls -l":
            return "mock_ls_output", "", 0
        elif command == "mkdir new_dir":
            return "", "", 0
        elif command == "rm test_file.txt":
            return "", "", 0
        elif command.startswith("echo 'Mock command for:"):
            return "", "", 0 # Mock echo commands as successful
        elif command == "mkdir new_folder":
            return "", "", 0
        else:
            return f"Mock command not recognized: {command}", "", 1

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y') # Auto-confirm execution
def test_list_files_mock_provider(mock_input):
    # Test with mock provider for 'list files'
    # We capture stdout to verify the output of run_nlba
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files in current directory", provider="mock", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: list files in current directory" in output
    assert "Generated command: ls -l" in output
    assert "STDOUT:\nmock_ls_output" in output
    assert "Exit Code: 0" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_create_directory_mock_provider(mock_input):
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("create directory new_dir", provider="mock", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: create directory new_dir" in output
    assert "Generated command: mkdir new_dir" in output
    assert "Exit Code: 0" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_remove_file_mock_provider(mock_input):
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("remove file test_file.txt", provider="mock", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: remove file test_file.txt" in output
    assert "Generated command: rm test_file.txt" in output
    assert "Exit Code: 0" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('nlba.llm_interface.GeminiLLMProvider.generate_command', return_value='ls -l')
@patch('builtins.input', return_value='y')
def test_list_files_gemini_provider(mock_input, mock_gemini_generate_command):
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files in current directory", provider="gemini", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: list files in current directory" in output
    assert "Generated command: ls -l" in output
    assert "STDOUT:\nmock_ls_output" in output
    assert "Exit Code: 0" in output
    mock_gemini_generate_command.assert_called_once_with("list files in current directory")

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('nlba.llm_interface.OpenAILLMProvider.generate_command', return_value='mkdir new_folder')
@patch('builtins.input', return_value='y')
def test_create_folder_openai_provider(mock_input, mock_openai_generate_command):
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("create a new folder called new_folder", provider="openai", skip_confirmation=True)
    output = f.getvalue()

    assert "Your request: create a new folder called new_folder" in output
    assert "Generated command: mkdir new_folder" in output
    assert "Exit Code: 0" in output
    mock_openai_generate_command.assert_called_once_with("create a new folder called new_folder")
