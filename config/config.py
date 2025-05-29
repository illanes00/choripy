from hydra import compose, initialize
from . import ROOT, DEFAULTS

def get_cfg(overrides: list[str] | None = None):
    with initialize(version_base=None, config_path="conf/hydra"):
        cfg = compose(config_name="config", overrides=overrides or [])
    return cfg

if __name__ == "__main__":
    print(get_cfg())
