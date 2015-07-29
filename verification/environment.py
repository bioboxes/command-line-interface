import os
import os.path as pt
from scripttest import TestFileEnvironment

root_dir = pt.abspath(pt.join(pt.dirname(__file__), '..'))

def before_scenario(context, _):
    tmp         = pt.join(root_dir, "tmp")
    context.env = TestFileEnvironment(base_path = tmp)

    # Required to work with boot2docker
    os.environ['TMPDIR'] = pt.join(root_dir, "tmp")
