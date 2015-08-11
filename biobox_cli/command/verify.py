"""
biobox verify - Verify that a Docker image matches the given specification type

Usage:
    biobox verify <biobox_type> <image> [--task=TASK]

Options:
  -h, --help             Show this screen.
  -t TASK --task=TASK    Specify which biobox task to test. [default: default]

Available Biobox types:

  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util as util
import sys, os, os.path, tempfile

def verification_file(biobox):
    file_ = biobox + '.feature'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'verification', file_))

def tmp_feature_dir():
    return os.path.abspath(os.path.join(os.getcwd(), 'biobox_verify'))

def run(argv):
    opts   = util.parse_docopt(__doc__, argv, False)
    biobox = opts['<biobox_type>']
    image  = opts['<image>']
    task   = opts['--task']

    from behave.__main__ import main as behave_main
    _, tmp_file = tempfile.mkstemp()
    cmd = "{file} --define IMAGE={image} --define TASK={task} --define TMP_DIR={tmp_dir} --outfile {tmp_file} --no-summary --stop"
    args = {'file':     verification_file(biobox),
            'tmp_dir':  tmp_feature_dir(),
            'image':    image,
            'tmp_file': tmp_file,
            'task':     task}

    behave_main(cmd.format(**args))

    with open(tmp_file, 'r') as f:
        output = f.read()

    if "Assertion Failed" in output:
        util.err_exit('failed_verification', {'image': image, 'biobox': biobox.replace('_', ' ')})
