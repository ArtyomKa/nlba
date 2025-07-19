import yaml
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "nlba"
HISTORY_FILE = CONFIG_DIR / "history.log"
GLOBAL_CONFIG_FILE = CONFIG_DIR / "config.yaml"
LOCAL_CONFIG_FILE = Path("./.nlba/config.yaml")

def get_history_file_path():
    return HISTORY_FILE

def log_request(request: str):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'a') as f:
        f.write(request + '\n')

def get_history_entry(index: int):
    if not HISTORY_FILE.exists():
        return None
    with open(HISTORY_FILE, 'r') as f:
        lines = f.readlines()
        if 1 <= index <= len(lines):
            return lines[index - 1].strip()
    return None


def load_config():
    config = {'nlba': {'provider': 'mock', 'summarize': False}}
    
    # Load global config
    if GLOBAL_CONFIG_FILE.exists():
        with open(GLOBAL_CONFIG_FILE, 'r') as f:
            global_config = yaml.safe_load(f)
            if global_config:
                config.update(global_config)

    # Load local config, overriding global
    if LOCAL_CONFIG_FILE.exists():
        with open(LOCAL_CONFIG_FILE, 'r') as f:
            local_config = yaml.safe_load(f)
            if local_config:
                config.update(local_config)
                
    return config

def save_config(config_data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(GLOBAL_CONFIG_FILE, 'w') as f:
        yaml.dump(config_data, f)
