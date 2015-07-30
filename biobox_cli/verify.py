import sys, os, os.path

def verification_file(biobox):
    file_ = biobox + '.feature'
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'verification', file_))

def tmp_feature_dir():
    return os.path.abspath(os.path.join(os.getcwd(), 'biobox_verify'))

def run(biobox, opts):
    from behave.__main__ import main as behave_main
    cmd = "{} --define TMP_DIR={} --define IMAGE={} --outfile /dev/null --no-summary"
    behave_main(cmd.format(verification_file(biobox), tmp_feature_dir(), opts['<image>']))

