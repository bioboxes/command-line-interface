import nose.tools      as nose
import biobox_cli.main as bbx

def test_select_biobox_with_valid_module():
    import biobox_cli.type.short_read_assembler as sra
    module   = "short_read_assembler"
    returned = bbx.select_biobox([module, "dummy"])
    nose.assert_equal(returned, sra)
