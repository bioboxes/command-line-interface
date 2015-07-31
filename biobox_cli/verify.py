import sys, os, os.path, tempfile

import biobox_cli.util as util

def verification_file(biobox):
    file_ = biobox + '.feature'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'verification', file_))

def tmp_feature_dir():
    return os.path.abspath(os.path.join(os.getcwd(), 'biobox_verify'))

def run(biobox, opts):
    image = opts['<image>']

    from behave.__main__ import main as behave_main
    _, tmp_file = tempfile.mkstemp()
    cmd = "{} --define TMP_DIR={} --define IMAGE={} --outfile {} --no-summary --stop"
    behave_main(cmd.format(verification_file(biobox), tmp_feature_dir(), image, tmp_file))

    with open(tmp_file, 'r') as f:
        output = f.read()

    if " Assertion Failed" in output:
        msg = "Verification failed - {} is not a valid biobox {}."
        util.err_exit(msg.format(image, biobox.replace('_', ' ')))
