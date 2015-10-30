import biobox_cli.container   as ctn
import biobox_cli.biobox_file as fle

import os
from biobox_cli.biobox import Biobox

class Assembler_Benchmark(Biobox):

    def copy_result_files(self, biobox_output_dir, dst):
        import shutil
        output_files = os.listdir(biobox_output_dir)
        map(lambda f: shutil.move(os.path.join(biobox_output_dir,f), dst), output_files)

    def prepare_volumes(self, opts, host_dst_dir):
        fasta_file = opts['--input-fasta']
        ref_dir = opts['--input-ref']

        host_src_fasta_file = os.path.abspath(fasta_file)
        host_src_ref_dir = os.path.abspath(ref_dir)

        cntr_src_fasta = "/fasta/input.fa"
        fasta_values = [(cntr_src_fasta, "contig")]
        fasta_yaml_values = fle.fasta_arguments(fasta_values)

        cntr_src_ref_dir = "/ref"
        ref_dir_yaml_values = fle.reference_argument(ref_dir)

        biobox_yaml = fle.generate([fasta_yaml_values, ref_dir_yaml_values])

        volume_strings = [
                ctn.volume_string(host_src_fasta_file, cntr_src_fasta),
                ctn.volume_string(host_src_ref_dir, cntr_src_ref_dir),
                ctn.biobox_file_volume_string(fle.create_biobox_directory(biobox_yaml)),
                ctn.output_directory_volume_string(host_dst_dir)]
        return volume_strings

    def get_doc(self):
        return """
Usage:
    biobox run assembler_benchmark <image> [--no-rm] --input-fasta=FILE --input-ref=DIR --output=DIR [--task=TASK]

Options:
  -h, --help                     Show this screen.
  -v, --version                  Show version.
  -if FILE, --input-fasta=FILE   Source FASTA file
  -ir DIR, --input-ref=DIR       Source directory containing reference fasta files
  -o DIR --output=DIR            Destination output directory
  -t TASK, --task=TASK           Optionally specify a biobox task to run [default: default]

"""

    def after_run(self, output, host_dst_dir):
        self.copy_result_files(host_dst_dir, output)