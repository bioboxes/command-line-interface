"""
biobox verify - Verify that a Docker image matches the given specification type

Usage:
    biobox verify <biobox_type> <image> [<args>...]

Options:
  -h, --help     Show this screen.

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

    from behave.__main__ import main as behave_main
    _, tmp_file = tempfile.mkstemp()
    cmd = "{} --define TMP_DIR={} --define IMAGE={} --outfile {} --no-summary --stop"
    behave_main(cmd.format(verification_file(biobox), tmp_feature_dir(), image, tmp_file))

    with open(tmp_file, 'r') as f:
        output = f.read()

    if "Assertion Failed" in output:
        util.err_exit('failed_verification', {'image': image, 'biobox': biobox.replace('_', ' ')})
