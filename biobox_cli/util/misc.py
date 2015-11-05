import sys
import inspect
import biobox_cli.util.error as error

def select_module(module, name):
    """
    Select and return a biobox module
    """
    mod_name = ".".join(["biobox_cli", module, name])
    try:
        __import__(mod_name)
    except ImportError:
        error.err_exit('unknown_command',
                {'command_type': str.replace(module, '_', ' '), 'command': name})
    return sys.modules[mod_name]

def parse_docopt(doc, argv, is_main_module):
    from docopt             import docopt
    from biobox_cli.version import __version__
    return docopt(doc,
                  argv          = argv,
                  version       = __version__,
                  options_first = is_main_module)

# http://stackoverflow.com/a/600612
def mkdir_p(path):
    import os, errno
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
    return os.path.abspath(path)

def get_subclasses(mod, cls):
    """Yield the classes in module ``mod`` that inherit from ``cls``"""
    for name, obj in inspect.getmembers(mod):
        if hasattr(obj, "__bases__") and cls in obj.__bases__:
            yield obj