import os
import os.path as pt
from scripttest import TestFileEnvironment

def before_scenario(context, _):
    root_dir = pt.abspath(pt.join(pt.dirname(__file__), '..'))

    path        = ":" + pt.join(root_dir, 'bin')
    tmp         = pt.join(root_dir, "tmp", "feature")
    python_path = pt.join(root_dir, 'vendor', 'python', 'lib', 'python2.7', 'site-packages')

    os.environ['PATH']       = path + ":" + os.environ['PATH']
    os.environ['PYTHONPATH'] = python_path
    context.env = TestFileEnvironment(base_path = tmp)
