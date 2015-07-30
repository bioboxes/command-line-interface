def run(opts):
    from behave.__main__ import main as behave_main
    import sys, os
    path = os.path.join(os.path.dirname(__file__), '..', 'verification', 'short_read_assembler.feature')
    tmp_dir = os.path.abspath(os.path.join(os.getcwd(), 'biobox_verify'))
    behave_main("{} --define TMP_DIR={} --outfile /dev/null --no-summary".format(os.path.abspath(path), tmp_dir))

