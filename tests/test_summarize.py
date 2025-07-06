import pytest
from unittest.mock import patch
from nlba.nlba import run_nlba, main
import io
from contextlib import redirect_stdout
import re

class MockCommandExecutor:
    def execute_command(self, command: str) -> tuple[str, str, int]:
        if command == "ls -l":
            return "total 0", "", 0
        else:
            return f"Mock command not recognized: {command}", "", 1

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_summarize_output_flag(mock_input):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files", provider="mock", skip_confirmation=True, summarize=True)
    output = f.getvalue()

    assert "--- Summary ---" in output
    assert "This is a mock summary for the command: 'ls -l'" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
@patch('nlba.config_manager.load_config', return_value={'nlba': {'summarize': True, 'provider': 'mock'}})
@patch('nlba.llm_interface.MockLLMProvider.summarize_output', return_value="This is a mock summary for the command: 'ls -l'")
def test_summarize_output_config(mock_summarize_output, mock_load_config, mock_input):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files", provider="mock", skip_confirmation=True, summarize=True)
    output = f.getvalue()

    assert "--- Summary ---" in output
    assert "This is a mock summary for the command: 'ls -l'" in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('builtins.input', return_value='y')
def test_no_summarize_output_by_default(mock_input):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files", provider="mock", skip_confirmation=True)
    output = f.getvalue()

    assert "--- Summary ---" not in output

@patch('nlba.nlba.CommandExecutor', new=MockCommandExecutor)
@patch('nlba.llm_interface.GeminiLLMProvider.summarize_output', return_value='The command `ls -l` executed successfully, showing an empty directory.')
@patch('nlba.llm_interface.GeminiLLMProvider.generate_command', return_value=('ls -l', 'non-destructive'))
@patch('builtins.input', return_value='y')
def test_summarize_output_gemini_provider(mock_input, mock_gemini_generate_command, mock_gemini_summarize_output):
    f = io.StringIO()
    with redirect_stdout(f):
        run_nlba("list files", provider="gemini", skip_confirmation=True, summarize=True)
    output = f.getvalue()

    assert "--- Summary ---" in output
    assert 'The command `ls -l` executed successfully, showing an empty directory.' in output
    mock_gemini_summarize_output.assert_called_once_with("list files", "ls -l", "total 0")
