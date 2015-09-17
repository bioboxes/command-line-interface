"""
Usage:
    biobox run short_read_assembler <image> [--no-rm] --input=FILE --output=FILE [--task=TASK]

Options:
  -h, --help              Show this screen.
  -v, --version           Show version.
  -i FILE, --input=FILE   Source FASTQ file containing paired short reads
  -o FILE, --output=FILE  Destination FASTA file for assembled contigs
  -t TASK, --task=TASK    Optionally specify a biobox task to run [default: default]
  -r, --no-rm             Don't remove the container after the process finishes

"""

import biobox_cli.container   as ctn
import biobox_cli.util.misc   as util
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
    task        = opts['--task']

    ctn.exit_if_no_image_available(image)

    cntr_fastq_file = "/fastq/input.fq.gz"
    fastq_values = [(cntr_fastq_file, "paired")]
    biobox_yaml = fle.generate([fle.fastq_arguments(fastq_values)])

    host_src_dir = os.path.abspath(fastq_file)
    host_dst_dir = tmp.mkdtemp()

    mount_strings = [
        ctn.mount_string(host_src_dir, cntr_fastq_file),
        ctn.biobox_file_mount_string(fle.create_biobox_directory(biobox_yaml)),
        ctn.output_directory_mount_string(host_dst_dir)]

    ctnr = ctn.create(image, task, mount_strings)
    ctn.run(ctnr)
    biobox_output = fle.parse(host_dst_dir)
    copy_contigs_file(host_dst_dir, biobox_output, contig_file)
    return ctnr

def remove(container):
    """
    Removes a container
    Note this method is not tested due to limitations of circle ci
    """
    ctn.remove(container)
