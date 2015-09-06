import yaml, os.path, sys

def err_message(msg_key, locals_):
    from pkg_resources import resource_string
    errors = yaml.load(resource_string(__name__, os.path.join('..', 'assets', 'error_messages.yml')))
    return errors[msg_key].format(**locals_)

def err_exit(msg_key, locals_):
    sys.stderr.write(err_message(msg_key, locals_))
    exit(1)
