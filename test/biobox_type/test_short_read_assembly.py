import pytest, tempfile, os.path
import helper
import biobox_cli.command.run as biobox

from biobox_cli.biobox_type.short_read_assembler import Assembler as interface

def create_args(output):
    return ["run",
            "short_read_assembler",
            helper.test_image(),
            "--task=short-read-assembler",
            "--input={}".format(helper.verification_file('short_read_assembler/genome_paired_reads.fq.gz')),
            "--output={}".format(output),
            "--no-rm"]

@pytest.mark.slow
def test_short_read_assembler():
    path = tempfile.mkdtemp()
    biobox.run(create_args(path))
    expected = os.path.join(path, "contigs.fa")
    assert os.path.isfile(expected)


def test_short_read_assembler_with_missing_input_file():
    from biobox_cli.exception import InputFileNotFound
    args = create_args(tempfile.mkdtemp())
    args[4] = '--input=missing-file'
    with pytest.raises(InputFileNotFound) as excp:
        interface().parse_opts(args)
