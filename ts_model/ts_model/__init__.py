import os
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class BaseMixin(dict):
    def __getattr__(self, attr):
        if attr in [column.key for column in self.__table__.columns]:
            return self.__getitem__(attr)
        else:
            return Base.__getattr__(self, attr)

    def __setattr__(self, key, value):
        if key in [column.key for column in self.__table__.columns]:
            self.__setitem__(key, value)
        Base.__setattr__(self, key, value)

    @sa.orm.reconstructor
    def reconstruct(self):
        for column in [column.key for column in self.__table__.columns]:
            self.__setitem__(column, Base.__getattribute__(self, column))

class DictMixin(dict):
    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)


packages = [os.path.basename(f)[:-3] for f in os.listdir(os.path.dirname(__file__)) if f[-3:] == ".py" and not f.endswith("__init__.py")]
for p in packages:
    exec(f"from .{p} import *")


