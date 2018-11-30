import enum

class Status(enum.IntEnum):
    ERROR = -1
    NONE = 0
    READYING = 1
    READY = 2
    def __get__(self, instance, owner):
        return self.value
    def __repr__(self):
        return self.name
