import sys
import biobox_cli.util.error  as error

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
