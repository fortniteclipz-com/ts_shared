import os
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

packages = [os.path.basename(f)[:-3] for f in os.listdir(os.path.dirname(__file__)) if f[-3:] == ".py" and not f.endswith("__init__.py")]
for p in packages:
    exec(f"from .{p} import *")


