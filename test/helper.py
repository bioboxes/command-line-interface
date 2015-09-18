import os
import biobox_cli.container as ctn

def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def is_ci_server():
    return "CI" in os.environ.keys()

def remove_container(container):
    if not is_ci_server():
        ctn.remove(container)
