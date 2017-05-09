import pytest, tempfile, os.path
import helper
import biobox_cli.command.run as biobox

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
    args = create_args(tempfile.mkdtemp())
    args[5] = '--input=missing-file'
    with pytest.raises(SystemExit) as excp:
        biobox.run(args)
