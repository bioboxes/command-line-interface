"""
Usage:
    biobox short_read_assembler <image> --input=FILE --output=FILE
    biobox short_read_assembler <image> --verify

Options:
  -h, --help              Show this screen.
  -v, --version           Show version.
  -i FILE, --input=FILE   Source FASTQ file containing paired short reads
  -o FILE, --output=FILE  Destination FASTA file for assembled contigs
  --verify, -f            Test whether an assembler image is biobox-compatible

"""

import biobox_cli.container   as ctn
import biobox_cli.util        as util
import biobox_cli.biobox_file as fle
import biobox_cli.verify      as verify

import os
import tempfile as tmp

def run(argv):
    opts = util.command_line_args(__doc__, argv, False)
    if opts['--verify']:
        verify.run('short_read_assembler', opts)
    else:
        run_container(opts)

def run_container(opts):
    image       = opts['<image>']
    fastq_file  = opts['--input']
    contig_file = opts['--output']

    if not ctn.image_available(image):
        msg = "No Docker image available with the name: {}\nDid you include the namespace too? E.g. bioboxes/velvet."
        util.err_exit(msg.format(image))


    cntr_src_dir = "/fastq"
    biobox_yaml = fle.generate([
        fle.fastq_arguments(cntr_src_dir, [fastq_file, "paired"])])

    host_src_dir = os.path.abspath(os.path.dirname(fastq_file))
    host_dst_dir = tmp.mkdtemp()

    mounts = [
        ctn.mount_string(host_src_dir, cntr_src_dir),
        ctn.biobox_file_mount_string(fle.create_biobox_directory(biobox_yaml)),
        ctn.output_directory_mount_string(host_dst_dir)]

    ctn.run(ctn.create(image, "default", mounts))

    with open(os.path.join(host_dst_dir, 'biobox.yaml'),'r') as f:
        import yaml
        output = yaml.load(f.read())

    contigs = output['arguments'][0]['fasta'][0]['value']
    import shutil
    shutil.move(os.path.join(host_dst_dir, contigs), contig_file)
