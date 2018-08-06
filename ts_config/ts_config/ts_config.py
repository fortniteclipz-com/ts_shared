import os
import functools
import yaml

dir_path = os.path.dirname(os.path.abspath(__file__))
yml_path = f"{dir_path}/ts_config.yml"
with open(yml_path) as f:
    cfg = yaml.safe_load(f)

def get(key):
    try:
        return functools.reduce(lambda c, k: c[k], key.split('.'), cfg)
    except Exception as e:
        return None

__all__ = ['get']
