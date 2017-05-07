import os, os.path
import biobox_cli.container as ctn

def test_image():
    return 'bioboxes/crash-test-biobox@sha256:fdfdda8192dd919e6cac37366784ec8cfbf52c6fec53fe942a7f1940bd7642e8'

def project_root():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def verification_file(path):
    return os.path.join(project_root(), "biobox_cli", "verification", "data", path)

def is_ci_server():
    return "CI" in os.environ.keys()

def remove_container(container):
    if not is_ci_server():
        ctn.remove(container)

def assert_file_not_empty(file_):
    file_size = os.stat(file_).st_size
    assert file_size != 0, "File should not be empty but is: {}".format(file_)

def assert_file_contents_equal(file_, contents):
    with open(file_, 'r') as f:
        assert f.read() == contents
