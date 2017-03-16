"""
Usage:
    biobox run short_read_assembler <image> [--memory=MEM] [--cpu-shares=CPU] [--cpuset=CPU] [--no-rm] --input=FILE --output=FILE [--task=TASK]

Options:
-h, --help                Show this screen.
-v, --version             Show version.
-i FILE, --input=FILE     Source FASTQ file containing paired short reads
-o FILE, --output=FILE    Destination FASTA file for assembled contigs
-t TASK, --task=TASK      Optionally specify a biobox task to run [default: default]
-r, --no-rm               Don't remove the container after the process finishes
-c=CPU, --cpu-shares=CPU  CPU shares (relative weight)
-s=CPU, --cpuset=CPU      CPUs that should be used. E.g:0,1 or 0-1
-m=MEM, --memory=MEM      RAM that should be used
"""

import biobox_cli.biobox_file as fle
from biobox_cli.biobox_helper import Biobox

import os

class Assembler(Biobox):

    def copy_contigs_file(self,biobox_output_dir, biobox_output, dst):
        contigs = biobox_output['arguments'][0]['fasta'][0]['value']
        src = os.path.join(biobox_output_dir, contigs)
        import shutil
        shutil.move(src, dst)

    def prepare_config(self, opts):
        return [
            {"fastq": [
                {"id": 0, "type": "paired", "value": opts['--input']}]}]

    def get_version(self):
        return "0.9.0"

    def after_run(self, output, host_dst_dir):
        biobox_output = fle.get_biobox_file_contents(host_dst_dir)
        self.copy_contigs_file(host_dst_dir, biobox_output, output)
