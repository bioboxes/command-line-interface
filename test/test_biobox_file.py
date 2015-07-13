import nose.tools             as nt
import biobox_cli.biobox_file as bbf

def test_generate_biobox_file():
    args = [{"fastq" : [{"id" : "i" , "value" : "v", "type": "t"}]}]
    output = bbf.generate(args)
    expected = """\
arguments:
- fastq:
  - id: i
    type: t
    value: v
version: 0.9.0
"""
    nt.assert_equal(expected, output)
