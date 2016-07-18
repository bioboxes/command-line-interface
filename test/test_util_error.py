import biobox_cli.util.error as error

def test_error_message():
    expected = """\
No Docker image available with the name: image
Did you include the namespace too? E.g. bioboxes/velvet.
"""
    assert expected == error.err_message('unknown_image', {'image': 'image'})
