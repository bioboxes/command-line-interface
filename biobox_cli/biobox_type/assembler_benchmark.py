"""
Usage:
    biobox run assembler_benchmark <image> --input-fasta=FILE --input-ref=DIR --output=FILE [--task=TASK]

Options:
  -h, --help                     Show this screen.
  -v, --version                  Show version.
  -if FILE, --input-fasta=FILE   Source FASTA file
  -ir DIR, --input-ref=DIR       Source directory containing reference fasta files
  -o DIR --output=FILE           Destination output directory
  -t TASK, --task=TASK           Optionally specify a biobox task to run [default: default]

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
    image = opts['<image>']
    fasta_file = opts['--input-fasta']
    ref_dir = opts['--input-ref']
    output_dir = opts['--output']
    task = opts['--task']

    if not ctn.image_available(image):
         util.err_exit('unknown_image', {'image': image})

    cntr_src_fasta_dir = "/fasta"
    fasta_yaml_values = fle.fasta_arguments(cntr_src_fasta_dir, [fasta_file, "contig"])

    cntr_src_ref_dir = "/ref"
    ref_dir_yaml_values = fle.reference_argument(cntr_src_ref_dir, ref_dir)

    biobox_yaml = fle.generate([fasta_yaml_values, ref_dir_yaml_values])

    host_src_fasta_file = os.path.abspath(fasta_file)
    host_src_ref_dir = os.path.abspath(ref_dir)
    host_dst_dir = tmp.mkdtemp()

    mount_strings = [
         ctn.mount_string(host_src_fasta_file, cntr_src_fasta_dir),
         ctn.mount_string(host_src_ref_dir, cntr_src_ref_dir),
         ctn.biobox_file_mount_string(fle.create_biobox_directory(biobox_yaml)),
         ctn.output_directory_mount_string(host_dst_dir)]

    ctn.run(ctn.create(image, task, mount_strings))
    biobox_output = fle.parse(host_dst_dir)
    copy_contigs_file(host_dst_dir, biobox_output, output_dir)