# Natural Language Bash Assistant (NLBA) - Tasks

## Performed Tasks
1. [x] Defined the project goal and initial scope for the "Natural Language Bash Assistant (NLBA)" project.
2. [x] Created the initial `nlba.py` file (`src/nlba/nlba.py`) with a basic CLI structure, mock LLM interaction, and mock command execution.
3. [x] Created the `ai` directory (`ai/`).
4. [x] Created `project.md` (`ai/project.md`) containing the project description.
5. [x] Implemented actual command execution using Python's `subprocess` module in `src/nlba/nlba.py`.


## MVP2
1. [x] Implement command modification indication (color-coding) based on LLM classification.
2. [x] Implement Basic Command History (view and re-execute past commands).

3. [x] Implement Configuration Persistence (save and load preferred LLM provider).
  3.1. [x] Add `PyYAML` dependency:
    3.1.1. [x] Add `pyyaml` to `dependencies` in `pyproject.toml`.
    3.1.2. [x] Run `uv pip install -e .` to install the new dependency.
  3.2. [x] Implement Configuration Loading Logic:
    3.2.1. [x] Create a new module (`src/nlba/config_manager.py`) to handle config loading/saving.
    3.2.2. [x] In `config_manager.py`, define functions to:
      3.2.2.1. [x] Get the global config path (`~/.config/nlba/config.yaml`).
      3.2.2.2. [x] Get the local config path (`./.nlba/config.yaml`).
      3.2.2.3. [x] Load configuration from both paths, with local overriding global.
      3.2.2.4. [x] Handle cases where config files or directories don't exist.
  3.3. [x] Implement Configuration Saving Logic:
    3.3.1. [x] In `config_manager.py`, define a function to save the current configuration to the global config file.
  3.4. [x] Integrate into `nlba.py`:
    3.4.1. [x] Import `config_manager`.
    3.4.2. [x] In `main()`, load the configuration at startup.
    3.4.3. [x] Modify `argparse` to:
      3.4.3.1. [x] Add a `--set-provider` argument to save the provider.
      3.4.3.2. [x] Use the loaded configuration's provider as the default, if no `--provider` argument is given.
      3.4.3.3. [x] Ensure `--provider` argument overrides the loaded config.
  3.5. [x] Update `ai/project.md`: Add details about configuration persistence and the two config file locations.
  3.6. [x] Add Tests to `tests/test_nlba.py`:
    3.6.1. [x] Test loading from global config.
    3.6.2. [x] Test loading from local config (overriding global).
    3.6.3. [x] Test saving provider to global config.
    3.6.4. [x] Test `--provider` argument overriding config.
    3.6.5. [x] Clean up created config files after tests.

## MVP3
1. [x] Implement Command Result Interpretation and Natural Language Summary
   1.1. [x] Extend the CLI to optionally pass command output back to the LLM after execution.
   1.2. [x] Update the LLM interface to accept command output as input and generate a natural language summary.
   1.3. [x] Modify the main CLI script (`nlba.py`) to display the LLM-generated summary alongside the command output.
   1.4. [x] Add a flag or configuration option to enable or disable this feature.
   1.5. [x] Write unit and integration tests covering:
       1.5.1. [x] Passing command output to the LLM.
       1.5.2. [x] Correct generation and display of the natural language summary.
       1.5.3. [x] Behavior when the feature is disabled.
   1.6. [x] Update `ai/files.md` if new modules or files are added.
   1.7. [x] Ensure all tests pass before marking the task as complete.
