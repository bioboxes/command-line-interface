import pytest, tempfile, os.path
import helper
import biobox_cli.command.run as biobox

from biobox_cli.biobox_type.assembler_benchmark import AssemblerBenchmark as interface

def create_args(output):
    return ["run",
            "assembler_benchmark",
            helper.test_image(),
            "--task=quast",
            "--input-fasta={}".format(helper.verification_file('assembler_benchmark/assembly.fasta')),
            "--input-ref={}".format(helper.verification_file('assembler_benchmark/references')),
            "--output={}".format(output),
            "--no-rm"]

@pytest.mark.slow
def test_assembly_benchmark_with_refs_and_existing_output():
    path = tempfile.mkdtemp()
    biobox.run(create_args(path))
    expected = os.path.join(path, "biobox.yaml")
    assert os.path.isfile(expected)


@pytest.mark.slow
def test_assembly_benchmark_with_refs_and_non_existing_output():
    path = os.path.join(tempfile.mkdtemp(), "quast")
    biobox.run(create_args(path))
    expected = os.path.join(path, "biobox.yaml")
    assert os.path.isfile(expected)


@pytest.mark.slow
def test_assembly_benchmark_with_no_refs():
    path = os.path.join(tempfile.mkdtemp(), "quast")
    args = create_args(path)
    del args[5] # Delete the reference from the input arg list
    biobox.run(args)
    expected = os.path.join(path, "biobox.yaml")
    assert os.path.isfile(expected)


def test_assembly_benchmark_with_missing_input_file():
    from biobox_cli.exception import InputFileNotFound
    args = create_args(tempfile.mkdtemp())
    args[4] = '--input-fasta=missing-file'
    with pytest.raises(InputFileNotFound) as excp:
        interface().parse_opts(args)
