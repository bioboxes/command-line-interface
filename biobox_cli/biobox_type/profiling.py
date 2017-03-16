"""
Usage:
    biobox run profiling <image> [--memory=MEM] [--cpu-shares=CPU] [--cpuset=CPU] [--no-rm] --input=FILE --inputDb=FILE --output=FILE [--task=TASK]

Options:
-h, --help                Show this screen.
-v, --version             Show version.
-i FILE, --input=FILE     Source FASTQ file containing paired short reads
-iDb, --inputDb=DIRECTORY NCBI TAXONOMY Directory
-o FILE, --output=FILE    Destination Profiling file
-t TASK, --task=TASK      Optionally specify a biobox task to run [default: default]
-r, --no-rm               Don't remove the container after the process finishes
-c=CPU, --cpu-shares=CPU  CPU shares (relative weight)
-s=CPU, --cpuset=CPU      CPUs that should be used. E.g:0,1 or 0-1
-m=MEM, --memory=MEM      RAM that should be used
"""

import os

import biobox_cli.biobox_file as fle
from biobox_cli.biobox_helper import Biobox


class Profiling(Biobox):
    def copy_profiling_file(self, biobox_output_dir, biobox_output, dst):
        profiling = biobox_output['arguments']['profiling'][0]['value']
        src = os.path.join(biobox_output_dir, profiling)
        import shutil
        shutil.move(src, dst)

    def prepare_config(self, opts):
        return [{
                "fastq": [
                    {"type": "fastq",
                     "value": opts['--input']
                     }
                ]
                },
                {
                "database": {
                        "value": opts['--inputDb'],
                        "type": "bioboxes.org:/taxonomy_ncbi_dumps"
                    }
                }
            ]

    def get_version(self):
        return "1.0.0"

    def after_run(self, output, host_dst_dir):
        pass
        biobox_output = fle.get_biobox_file_contents(host_dst_dir)
        self.copy_profiling_file(host_dst_dir, biobox_output, output)