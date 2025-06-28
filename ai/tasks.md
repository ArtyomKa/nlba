# Natural Language Bash Assistant (NLBA) - Tasks

## Performed Tasks
1. [x] Defined the project goal and initial scope for the "Natural Language Bash Assistant (NLBA)" project.
2. [x] Created the initial `nlba.py` file (`src/nlba/nlba.py`) with a basic CLI structure, mock LLM interaction, and mock command execution.
3. [x] Created the `ai` directory (`ai/`).
4. [x] Created `project.md` (`ai/project.md`) containing the project description.
5. [x] Implemented actual command execution using Python's `subprocess` module in `src/nlba/nlba.py`.


## MVP2
- [x] Implement command modification indication (color-coding) based on LLM classification.
- [ ] Implement Basic Command History (view and re-execute past commands).
- [ ] Implement Configuration Persistence (save and load preferred LLM provider).
  - [x] Add `PyYAML` dependency:
    - [x] Add `pyyaml` to `dependencies` in `pyproject.toml`.
    - [ ] Run `uv pip install -e .` to install the new dependency.
  - [x] Implement Configuration Loading Logic:
    - [x] Create a new module (`src/nlba/config_manager.py`) to handle config loading/saving.
    - [x] In `config_manager.py`, define functions to:
      - [x] Get the global config path (`~/.config/nlba/config.yaml`).
      - [x] Get the local config path (`./.nlba/config.yaml`).
      - [x] Load configuration from both paths, with local overriding global.
      - [x] Handle cases where config files or directories don't exist.
  - [x] Implement Configuration Saving Logic:
    - [x] In `config_manager.py`, define a function to save the current configuration to the global config file.
  - [x] Integrate into `nlba.py`:
    - [x] Import `config_manager`.
    - [x] In `main()`, load the configuration at startup.
    - [x] Modify `argparse` to:
      - [x] Add a `--set-provider` argument to save the provider.
      - [x] Use the loaded configuration's provider as the default, if no `--provider` argument is given.
      - [x] Ensure `--provider` argument overrides the loaded config.
  - [ ] Update `ai/project.md`: Add details about configuration persistence and the two config file locations.
  - [x] Add Tests to `tests/test_nlba.py`:
    - [x] Test loading from global config.
    - [x] Test loading from local config (overriding global).
    - [x] Test saving provider to global config.
    - [x] Test `--provider` argument overriding config.
    - [x] Clean up created config files after tests.
