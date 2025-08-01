# Natural Language Bash Assistant (NLBA) Project

## Project Goal
To create a command-line utility that translates natural language requests into executable bash commands, initially focusing on file system operations, and then executing them.

## Core Features (Initial Scope - MVP)
1.  **Natural Language Input:** Accept a user's request in plain English (e.g., "list all python files in the current directory").
2.  **LLM Command Generation:** Use an LLM to translate the natural language request into an appropriate bash command (e.g., `ls -l *.py`).
3.  **Command Preview & Confirmation:** Display the generated bash command to the user and ask for confirmation before execution.
4.  **Command Execution:** Execute the confirmed bash command.
5.  **Output Display:** Show the output of the executed command to the user.
6.  **Filesystem Operations (Initial Focus):** Prioritize commands related to `ls`, `cd`, `mkdir`, `rm`, `cp`, `mv`, `cat`, `grep`, `find`.

## Core Features (MVP2)
1. **Command Modification Indication:** Display the generated bash command in color to indicate whether it performs a modification (red) or is non-destructive (green).

2. **Interactive Shell Interface:** Implement a shell-like interface where the user can run `nlba` to enter an interactive prompt (`>`). Users can type natural language requests, receive generated bash commands with modification indication, confirm execution, and view command output in a continuous session.
## Core Features (MVP3)
1. **Command Result Interpretation and Natural Language Summary:** Optionally, after a command is executed, its output can be sent back to the LLM to generate a user-friendly, natural language summary. This feature can be enabled with a `--summarize` flag or through a configuration setting.

## Technology Stack
*   **Language:** Python
*   **LLM:** Placeholder for an LLM API (e.g., Gemini API, OpenAI API).
*   **Shell Interaction:** Python's `subprocess` module.
*   **CLI Framework:** `argparse` (initially).
*   **Package manager:** `uv`

## Testing
*   **Framework:** `pytest`
*   **Execution:** Tests are run using `uv run pytest` from the project root.

## Configuration Persistence
*   **Global Configuration:** `~/.config/nlba/config.yaml`
*   **Workspace Configuration:** `./.nlba/config.yaml` (overrides global settings)

### Details
- Configuration persistence allows saving and loading the preferred LLM provider.
- Two configuration file locations are supported:
  - Global config: `~/.config/nlba/config.yaml`
  - Workspace/local config: `./.nlba/config.yaml` (overrides global)
- The CLI supports a `--set-provider` argument to save the default provider.
- Configuration loading merges global and local configs, with local taking precedence.
- Configuration saving writes to the global config file.

## Project Structure
*   `src/nlba/nlba.py`: Main CLI script.
*   `src/nlba/llm_interface.py`: Handles communication with the LLM.
*   `src/nlba/command_executor.py`: Manages the execution of bash commands.
*   `ai/`: Directory for AI-related components and project documentation.
    *   `project.md`: This project description.
    *   `tasks.md`: List of performed and future tasks.
