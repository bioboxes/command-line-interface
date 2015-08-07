"""
Usage:
    biobox run short_read_assembler <image> --input=FILE --output=FILE

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

def copy_contigs_file(biobox_output_dir, biobox_output, dst):
    contigs = biobox_output['arguments'][0]['fasta'][0]['value']
    src = os.path.join(biobox_output_dir, contigs)
    import shutil
    shutil.move(src, dst)

def run(argv):
    opts = util.parse_docopt(__doc__, argv, False)
    image       = opts['<image>']
    fastq_file  = opts['--input']
    contig_file = opts['--output']

    if not ctn.image_available(image):
        util.err_exit('unknown_image', {'image': image})

    cntr_src_dir = "/fastq"
    biobox_yaml = fle.generate([
        fle.fastq_arguments(cntr_src_dir, [fastq_file, "paired"])])

    host_src_dir = os.path.abspath(os.path.dirname(fastq_file))
    host_dst_dir = tmp.mkdtemp()

    mount_strings = [
        ctn.mount_string(host_src_dir, cntr_src_dir),
        ctn.biobox_file_mount_string(fle.create_biobox_directory(biobox_yaml)),
        ctn.output_directory_mount_string(host_dst_dir)]

    ctn.run(ctn.create(image, "default", mount_strings))
    biobox_output = fle.parse(host_dst_dir)
    copy_contigs_file(host_dst_dir, biobox_output, contig_file)
