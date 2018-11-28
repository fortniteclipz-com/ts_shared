import os
import functools
import yaml

ts_env = os.environ.get('ts_env', 'dev')
print("ts_config | ts_env |", ts_env)

dir_path = os.path.dirname(os.path.abspath(__file__))
yml_path = f"{dir_path}/ts_config_{ts_env}.yml"
with open(yml_path) as f:
    cfg = yaml.safe_load(f)

def get(key):
    try:
        return functools.reduce(lambda c, k: c[k], key.split('.'), cfg)
    except Exception as e:
        return None

__all__ = ['get']
