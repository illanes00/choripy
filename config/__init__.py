from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
with open(ROOT / "config" / "default.yml", "r") as f:
    DEFAULTS = yaml.safe_load(f)
