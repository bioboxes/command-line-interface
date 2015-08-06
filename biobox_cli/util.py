import sys

def select_module(module, name):
    """
    Select and return a biobox module
    """
    mod_name = ".".join(["biobox_cli", module, name])
    try:
        __import__(mod_name)
    except ImportError:
        msg = """\
Unknown {}: "{}".
Run `biobox --help` for a list of available.
"""
        err_exit(msg.format(str.replace(module, '_', ' '), name))
    return sys.modules[mod_name]

def parse_docopt(doc, argv, is_main_module):
    from docopt  import docopt
    from version import __version__
    return docopt(doc,
                  argv          = argv,
                  version       = __version__,
                  options_first = is_main_module)

def help_exit(doc, opts):
    if '--help' in opts:
        sys.stdout.write(doc)
        exit(0)

def err_exit(msg):
    sys.stderr.write(msg)
    exit(1)
