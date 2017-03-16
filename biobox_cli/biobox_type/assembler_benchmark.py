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

    def get_version(self):
        return "0.9.0"

    def prepare_config(self, opts):
        output = opts['--output']
        if not os.path.exists(output):
            os.makedirs(output)

        args = [{"fasta" : [ {"id": 0, "type": "contigs", "value": opts['--input-fasta']}]}]

        if opts['--input-ref']:
            return args + [{"fasta_dir": [ {"id": 1, "type": "references", "value": opts['--input-ref']} ] }]
        else:
            return args

    def after_run(self, output, host_dst_dir):
        self.copy_result_files(host_dst_dir, output)
