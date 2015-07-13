"""
Usage:
    biobox short_read_assembler <image> [options]

Options:
  -h, --help              Show this screen.
  -v, --version           Show version.
  -i FILE, --input=FILE   Source FASTQ file containing paired short reads
  -o FILE, --output=FILE  Destination FASTA file for assembled contigs

"""

import biobox_cli.container   as ctn
import biobox_cli.util        as util
import biobox_cli.biobox_file as fle
import os
import tempfile as tmp

def run(argv):
    opts  = util.command_line_args(__doc__, argv, False)

    image      = opts['<image>']
    fastq_file = opts['--input']

    if not ctn.image_available(image):
        msg = "No Docker image available with the name: {}"
        util.err_exit(msg.format(image))

    cntr_src_dir = "/fastq"
    cntr_dst_dir = "/assembly"

    host_src_dir = os.path.dirname(fastq_file)
    host_dst_dir = tmp.mkdtemp()

    biobox_args = fle.fastq_arguments(cntr_src_dir, [fastq_file, "paired"])
    biobox_path = fle.create_biobox_directory(fle.generate(biobox_args))
