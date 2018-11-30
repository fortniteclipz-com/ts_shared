import enum

class Status(enum.IntEnum):
    ERROR = -1
    NONE = 0
    WORKING = 1
    DONE = 2
    def __get__(self, instance, owner):
        return self.value
    def __repr__(self):
        return self.name
