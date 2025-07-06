import yaml
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "nlba"
GLOBAL_CONFIG_FILE = CONFIG_DIR / "config.yaml"
LOCAL_CONFIG_FILE = Path("./.nlba/config.yaml")

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
