import os
import functools
import yaml

TS_ENV = os.environ.get('TS_ENV', 'dev')
print("ts_config | TS_ENV |", TS_ENV)

dir_path = os.path.dirname(os.path.abspath(__file__))
yml_path = f"{dir_path}/ts_config_{TS_ENV}.yml"
with open(yml_path) as f:
    cfg = yaml.safe_load(f)

def get(key):
    try:
        return functools.reduce(lambda c, k: c[k], key.split('.'), cfg)
    except Exception as e:
        return None

__all__ = ['get']
