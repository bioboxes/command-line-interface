import os

def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def is_ci_server():
    return "CI" in os.environ.keys()

