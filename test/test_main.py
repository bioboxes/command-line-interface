import nose.tools      as nose
import biobox_cli.main as bbx

def test_select_biobox_with_valid_module():
    module   = "short_read_assembler"
    returned = bbx.select_biobox([module, "dummy"])
    expected = __import__("biobox_cli.type." + module)
    nose.assert_equal(returned, expected)
