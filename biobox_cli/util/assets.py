import os.path
from pkg_resources import resource_string

def get_asset_file_contents(file_):
    return resource_string(__name__, os.path.join('..', 'assets', file_))
