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

def test_fastq_arguments_with_single_arg():
    args = ["file_path", "paired"]
    expected = {"fastq" :
      [{"id" : "fastq_0", "type": "paired", "value" : "/mount/file_path"}]}
    nt.assert_equal(bbf.fastq_arguments("/mount", args), expected)
