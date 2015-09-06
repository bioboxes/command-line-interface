def get(key):
    def _get(_dict):
        if key in _dict:
            return _dict[key]
        else:
            return None
    return _get

def is_not_none(i):
    return (i is not None)

