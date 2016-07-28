import pytest, tempfile, helper
import biobox_cli.command.run as biobox


def create_args(output):
    return ["run",
            "short_read_assembler",
            "bioboxes/velvet",
            "--input={}".format(helper.verification_file('short_read_assembler/genome_paired_reads.fq.gz')),
            "--output={}".format(output)]

@pytest.mark.noci
@pytest.mark.slow
def test_short_read_assembler():
    # Will run the remove() function
    # Difficult to check this has worked though
    biobox.run(create_args(tempfile.mkdtemp()))
