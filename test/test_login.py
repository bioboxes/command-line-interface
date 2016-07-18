import biobox_cli.command.login as login
import helper                   as hlpr
import tempfile                 as tmp

import os.path
import shutil


TMP_DIR       = tmp.mkdtemp()
TMP_FILE_NAME = 'tmp_file'
TMP_PATH      = os.path.join(TMP_DIR, TMP_FILE_NAME)

def teardown_method(self, method):
    if os.path.exists(TMP_PATH):
        os.remove(TMP_PATH)


def test_get_login_parameters_with_unknown_type():
    assert None == login.get_login_parameters('unknown')


def test_create_login_file_literal():
    value = {'type': 'literal', 'src': 'literal_string', 'dst': TMP_FILE_NAME}
    login.create_login_file(TMP_DIR, value)
    hlpr.assert_file_contents_equal(TMP_PATH, 'literal_string')


def test_create_login_file_path():
    value = {'type': 'path', 'src': 'short_read_assembler/genome_paired_reads.fq.gz', 'dst': TMP_FILE_NAME}
    login.create_login_file(TMP_DIR, value)
    hlpr.assert_file_not_empty(TMP_PATH)


def test_create_login_volume():
    dst_dir = '/bbx/input'
    value   = [{'type': 'literal', 'src': 'literal_string', 'dst': TMP_FILE_NAME}]
    volume  = login.create_login_volume(dst_dir, value)

    dir_path = os.path.join(login.TEMPORARY_DIRECTORY, dst_dir.strip("/"))
    hlpr.assert_file_not_empty(os.path.join(dir_path, TMP_FILE_NAME))
    hlpr.assert_file_contents_equal(os.path.join(dir_path, TMP_FILE_NAME), 'literal_string')
    assert ':'.join([dir_path, dst_dir, 'rw']) in volume
