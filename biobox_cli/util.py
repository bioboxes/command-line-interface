import sys, yaml, os.path

def select_module(module, name):
    """
    Select and return a biobox module
    """
    mod_name = ".".join(["biobox_cli", module, name])
    try:
        __import__(mod_name)
    except ImportError:
        err_exit('unknown_command',
                {'command_type': str.replace(module, '_', ' '), 'command': name})
    return sys.modules[mod_name]

def parse_docopt(doc, argv, is_main_module):
    from docopt  import docopt
    from version import __version__
    return docopt(doc,
                  argv          = argv,
                  version       = __version__,
                  options_first = is_main_module)

def err_message(msg_key, locals_):
    from pkg_resources import resource_string
    errors = yaml.load(resource_string(__name__, os.path.join('assets', 'error_messages.yml')))
    return errors[msg_key].format(**locals_)

def err_exit(msg_key, locals_):
    sys.stderr.write(err_message(msg_key, locals_))
    exit(1)
