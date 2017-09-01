"""
Usage:
    biobox run unsupervised_binning_benchmark <image> [--memory=MEM] [--cpu-shares=CPU] [--cpuset=CPU] [--no-rm] --fasta=FILE  --labels=FILE --predictions=FILE --output=FILE [--task=TASK]

Options:
-h, --help                Show this screen.
-v, --version             Show version.
-p FILE, --predictions=FILE    Predictions made by a binning tool
-f, --fasta=FILE    Fasta file with a gold standard
-l, --labels=FILE    Gold standard binning file
-o FILE, --output=FILE    Destination metrics file
-t TASK, --task=TASK      Optionally specify a biobox task to run [default: default]
-r, --no-rm               Don't remove the container after the process finishes
-c=CPU, --cpu-shares=CPU  CPU shares (relative weight)
-s=CPU, --cpuset=CPU      CPUs that should be used. E.g:0,1 or 0-1
-m=MEM, --memory=MEM      RAM that should be used
"""

import os
import biobox_cli.biobox_file as fle
from biobox_cli.biobox_helper import Biobox


class UnsupervisedBinning(Biobox):
    def copy_profiling_file(self, biobox_output_dir, biobox_output, dst):
        profiling = biobox_output['results'][0]['value']
        src = os.path.join(biobox_output_dir, profiling)
        import shutil
        shutil.move(src, dst)

    def prepare_config(self, opts):
        return [{
                "fasta":
                    {"type": "contig",
                     "value": opts['--fasta']
                     }
                },
                {
                "labels": {
                        "value": opts['--labels'],
                        "type": "binning"
                    },
                },
                {
                "predictions": {
                        "value": opts['--predictions'],
                        "type": "binning"
                    }
                }
            ]

    def get_version(self):
        return "0.11.0"

    def after_run(self, output, host_dst_dir):
        pass
        biobox_output = fle.get_biobox_file_contents(host_dst_dir)
        self.copy_profiling_file(host_dst_dir, biobox_output, output)