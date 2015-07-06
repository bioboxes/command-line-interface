import os
from scripttest import TestFileEnvironment

def before_scenario(context, _):
    path = os.path.dirname(os.path.abspath(__file__))

    os.environ['PATH'] += ":" + os.path.join(path, '..', 'bin')
    os.environ['PYTHONPATH'] = os.path.join(path, '..', 'vendor', 'python', 'lib', 'python2.7', 'site-packages')
    context.env = TestFileEnvironment(base_path = 'tmp')
