import os
import os.path as pt
from scripttest import TestFileEnvironment

def before_scenario(context, _):
    root_dir = pt.abspath(pt.join(pt.dirname(__file__), '..'))

    path        = ":" + pt.join(root_dir, 'bin')
    tmp         = pt.join(root_dir, "tmp")
    python_path = pt.join(root_dir, 'vendor', 'python', 'lib', 'python2.7', 'site-packages')

    os.environ['PATH']       += path
    os.environ['PYTHONPATH'] = python_path
    os.environ['TMPDIR']     = tmp  # Required to work with boot2docker
    context.env = TestFileEnvironment(base_path = tmp)
