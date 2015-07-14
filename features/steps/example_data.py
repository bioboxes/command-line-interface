import helper as hp
import gzip
import os

@given(u'I have the example genome paired fastq file "{}"')
def step_impl(context, file_):
    path = os.path.dirname(os.path.realpath(__file__))
    data = os.path.join(path, '..', 'example_data', 'genome_paired_reads.fq')
    with open(data, 'r') as in_:
        with gzip.open(hp.get_file_path(context, file_), 'w') as out_:
            out_.write(in_.read().strip())
