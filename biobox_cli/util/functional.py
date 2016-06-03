try:
    from functools import reduce
except ImportError:
    pass

def get(key):
    """
    Function that returns a function that will look up the given key in a
    dictionary. Useful for mapping over a dictionary.
    """
    def _get(_dict):
        if key in _dict:
            return _dict[key]
        else:
            return None
    return _get

def thread(functions):
    """
    Threads a list of functions of over an initial argument. The argument
    should be the first item in the list.
    """
    return reduce(lambda x, f: f(x), functions)

def is_not_none(i):
    return (i is not None)

def is_not_empty(x):
    return not is_empty(x)

def is_empty(x):
    return len(list(x)) == 0

def first(x):
    return x[0]

# http://stackoverflow.com/a/480227/91144
def unique(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
