import enum

class Status(enum.IntEnum):
    NONE = 0
    INITIALIZING = 1
    READY = 2
    def __repr__(self):
        return self.name
