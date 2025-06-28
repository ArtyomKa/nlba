# Natural Language Bash Assistant (NLBA) - Tasks

## Performed Tasks
1. [x] Defined the project goal and initial scope for the "Natural Language Bash Assistant (NLBA)" project.
2. [x] Created the initial `nlba.py` file (`src/nlba/nlba.py`) with a basic CLI structure, mock LLM interaction, and mock command execution.
3. [x] Created the `ai` directory (`ai/`).
4. [x] Created `project.md` (`ai/project.md`) containing the project description.
5. [x] Implemented actual command execution using Python's `subprocess` module in `src/nlba/nlba.py`.

## MVP2
1. [x] Implement command modification indication (color-coding) based on LLM classification.
2. [ ] Implement Basic Command History (view and re-execute past commands).
3. [ ] Implement Configuration Persistence (save and load preferred LLM provider).
    3.1. **Add `PyYAML` dependency:**
        3.1.1. Add `pyyaml` to `dependencies` in `pyproject.toml`.
        3.1.2. Run `uv pip install -e .` to install the new dependency.
    3.2. **Implement Configuration Loading Logic:**
        3.2.1. Create a new module (`src/nlba/config_manager.py`) to handle config loading/saving.
        3.2.2. In `config_manager.py`, define functions to:
            3.2.2.1. Get the global config path (`~/.config/nlba/config.yaml`).
            3.2.2.2. Get the local config path (`./.nlba/config.yaml`).
            3.2.2.3. Load configuration from both paths, with local overriding global.
            3.2.2.4. Handle cases where config files or directories don't exist.
    3.3. **Implement Configuration Saving Logic:**
        3.3.1. In `config_manager.py`, define a function to save the current configuration to the global config file.
    3.4. **Integrate into `nlba.py`:**
        3.4.1. Import `config_manager`.
git rebase -i HEAD~2        3.4.2. In `main()`, load the configuration at startup.
        3.4.3. Modify `argparse` to:
            3.4.3.1. Add a `--set-provider` argument to save the provider.
            3.4.3.2. Use the loaded configuration's provider as the default, if no `--provider` argument is given.
            3.4.3.3. Ensure `--provider` argument overrides the loaded config.
    3.5. **Update `ai/project.md`**: Add details about configuration persistence and the two config file locations.
    3.6. **Add Tests to `tests/test_nlba.py`**:
        3.6.1. Test loading from global config.
        3.6.2. Test loading from local config (overriding global).
        3.6.3. Test saving provider to global config.
        3.6.4. Test `--provider` argument overriding config.
        3.6.5. Clean up created config files after tests.
