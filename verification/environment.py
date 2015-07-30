import os
import os.path as pt
from scripttest import TestFileEnvironment

root_dir = pt.abspath(pt.join(pt.dirname(__file__), '..'))

def before_scenario(context, _):
    tmp         = context.config.userdata["TMP_DIR"]
    context.env = TestFileEnvironment(base_path = tmp)

    os.environ['IMAGE'] = context.config.userdata["IMAGE"]

    # Mounting volumes in Docker needs an explict full path.
    # The path cannot be hard coded into the features as it varies
    # Therefore dynamically pass the full path prefix as an
    # environment variable.
    os.environ['TMPDIR'] = tmp
