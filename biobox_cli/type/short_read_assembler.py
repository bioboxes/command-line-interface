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
    cntr_dst_dir = "/bbx/output"
    cntr_yml_dir = "/bbx/input"

    biobox_args = fle.fastq_arguments(cntr_src_dir, [fastq_file, "paired"])

    # Need to ensure is always an absolute path
    host_src_dir = os.path.abspath(os.path.dirname(fastq_file))
    host_dst_dir = tmp.mkdtemp()
    host_yml_dir = fle.create_biobox_directory(fle.generate([biobox_args]))


    import docker.utils

    container = ctn.client().create_container(image, 'default',
      volumes     = [cntr_src_dir, cntr_dst_dir, cntr_yml_dir],
      host_config = docker.utils.create_host_config(binds=[
          ":".join([host_src_dir, cntr_src_dir, "ro"]),
          ":".join([host_yml_dir, cntr_yml_dir, "ro"]),
          ":".join([host_dst_dir, cntr_dst_dir, "rw"])
          ])
      )

    ctn.client().start(container.get("Id"))
