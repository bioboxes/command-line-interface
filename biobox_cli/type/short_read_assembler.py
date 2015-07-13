"""
Usage:
    biobox short_read_assembler <image> [options]

Options:
  -h, --help              Show this screen.
  -v, --version           Show version.
  -i FILE, --input=FILE   Source FASTQ file containing paired short reads
  -o FILE, --output=FILE  Destination FASTA file for assembled contigs

"""

import biobox_cli.container as ctn
import biobox_cli.util      as util
import os

def run(argv):
    opts  = util.command_line_args(__doc__, argv, False)
    image = opts['<image>']

    if not ctn.image_available(image):
        msg = "No Docker image available with the name: {}"
        util.err_exit(msg.format(image))
