import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
INVENTORY_FILE = PROJECT_ROOT / "inventory.yaml"

def load_config():
    with CONFIG_FILE.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_inventory():
    with INVENTORY_FILE.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)
