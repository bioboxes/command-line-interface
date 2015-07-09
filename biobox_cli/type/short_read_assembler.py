"""
Usage:
    biobox short_read_assembler <container> [options]

Options:
  -h, --help              Show this screen.
  -v, --version           Show version.
  -i FILE, --input=FILE   Source FASTQ file containing paired short reads
  -o FILE, --output=FILE  Destination FASTA file for assembled contigs

"""

import biobox_cli.util as util

def run(argv):
    opts = util.command_line_args(__doc__, argv, False)
