"""
Usage:
    biobox run assembler_benchmark <image> [--memory=MEM] [--cpu-shares=CPU_SHARES] [--cpuset=CPUS] [--no-rm] [--input-ref=DIR] --input-fasta=FILE --output=DIR [--task=TASK]

Options:
-h, --help                     Show this screen.
-v, --version                  Show version.
-f FILE, --input-fasta=FILE    Source FASTA file (Optional)
-i DIR, --input-ref=DIR        Source directory containing reference fasta files
-o DIR, --output=DIR            Destination output directory
-t TASK, --task=TASK           Optionally specify a biobox task to run [default: default]
-r, --no-rm                    Don't remove the container after the process finishes
-c=CPU, --cpu-shares=CPU       CPU shares (relative weight)
-s=CPU, --cpuset=CPU           CPUs that should be used. E.g:0,1 or 0-1
-m=MEM, --memory=MEM           RAM that should be used
"""

import biobox.image.volume    as vol
import biobox_cli.biobox_file as fle

import os
from biobox_cli.biobox_helper import Biobox

class Assembler_Benchmark(Biobox):

    def copy_result_files(self, biobox_output_dir, dst):
        import shutil
        output_files = os.listdir(biobox_output_dir)
        list(map(lambda f: shutil.move(os.path.join(biobox_output_dir,f), dst), output_files))

    def prepare_volumes(self, opts, host_dst_dir):
        fasta_file = opts['--input-fasta']
        ref_dir = opts['--input-ref']

        host_src_fasta_file = os.path.abspath(fasta_file)
        if ref_dir:
            host_src_ref_dir = os.path.abspath(ref_dir)

        cntr_src_fasta = "/fasta/input.fa"
        fasta_values = [(cntr_src_fasta, "contig")]
        fasta_yaml_values = fle.fasta_arguments(fasta_values)

        yaml_values = [fasta_yaml_values]
        if ref_dir:
            cntr_src_ref_dir = "/ref"
            ref_dir_yaml_values = fle.reference_argument(cntr_src_ref_dir)
            yaml_values.append(ref_dir_yaml_values)

        biobox_yaml = fle.generate(yaml_values)

        volume_strings = [
                vol.create_volume_string(host_src_fasta_file, cntr_src_fasta),
                vol.biobox_file(fle.create_biobox_directory(biobox_yaml)),
                vol.output(host_dst_dir)]

        if ref_dir:
            volume_strings.append(vol.create_volume_string(host_src_ref_dir, cntr_src_ref_dir))

        return volume_strings

    def after_run(self, output, host_dst_dir):
        self.copy_result_files(host_dst_dir, output)
