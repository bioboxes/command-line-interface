import os.path
from pkg_resources import resource_string, resource_filename

def get_asset_file_contents(file_):
    return resource_string(__name__, os.path.join('..', 'assets', file_))

def get_data_file_path(file_):
    return resource_filename(__name__, os.path.join('..', 'verification', 'data', file_))
