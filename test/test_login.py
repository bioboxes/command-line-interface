import nose.tools               as nose
import biobox_cli.command.login as login
import helper                   as hlpr
import tempfile                 as tmp

from os.path import join
from os      import stat

def test_get_login_parameters_with_unknown_type():
    nose.assert_equal(None, login.get_login_parameters('unknown'))

def test_create_login_file_literal():
    file_name = 'file_name'
    value = {'type': 'literal', 'src': 'literal_string', 'dst': file_name}
    directory = tmp.mkdtemp()
    login.create_login_file(directory, value)
    with open(join(directory, file_name)) as f:
        nose.assert_equal('literal_string', f.read())

def test_create_login_file_path():
    file_name = 'file_name'
    value = {'type': 'path', 'src': 'genome_paired_reads.fq.gz', 'dst': file_name}
    directory = tmp.mkdtemp()
    login.create_login_file(directory, value)
    file_size = stat(join(directory, file_name)).st_size
    nose.assert_not_equal(file_size, 0)
