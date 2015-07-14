
def command_line_args(doc, argv, is_main_module):
    from docopt  import docopt
    from version import __version__
    return docopt(doc,
                  argv          = argv,
                  version       = __version__,
                  options_first = is_main_module)

def err_exit(msg):
    import sys
    sys.stderr.write(msg)
    exit(1)
