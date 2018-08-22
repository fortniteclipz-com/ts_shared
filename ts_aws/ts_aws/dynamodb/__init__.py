import decimal

class Status(enum.IntEnum):
    INITIALIZING = 0
    READY = 1
    def __repr__(self):
        return self.name

def _replace_decimals(obj):
    if isinstance(obj, list):
        for i in range(len(obj)):
            obj[i] = _replace_decimals(obj[i])
        return obj
    elif isinstance(obj, dict):
        for k in obj.keys():
            obj[k] = _replace_decimals(obj[k])
        return obj
    elif isinstance(obj, decimal.Decimal):
        if obj % 1 == 0:
            return int(obj)
        else:
            return float(obj)
    else:
        return obj

def _replace_floats(obj):
    if isinstance(obj, list):
        obj = obj.copy()
        for i in range(len(obj)):
            obj[i] = _replace_floats(obj[i])
        return obj
    elif isinstance(obj, dict):
        obj = obj.copy()
        for k in list(obj.keys()):
            obj[k] = _replace_floats(obj[k])
            if obj[k] is None:
                del obj[k]
        return obj
    elif isinstance(obj, float):
        if obj % 1 == 0:
            return int(obj)
        else:
            return decimal.Decimal(str(obj))
    else:
        return obj

