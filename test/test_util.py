import nose.tools      as nt
import biobox_cli.util as util

def test_error_message():
    expected = """\
No Docker image available with the name: image
Did you include the namespace too? E.g. bioboxes/velvet.
"""
    nt.assert_equal(expected, util.err_message('unknown_image', {'image': 'image'}))
