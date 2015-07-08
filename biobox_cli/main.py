"""
biobox - A command line interface for running biobox Docker containers

Usage:
    biobox <biobox_type> <container> [options]

Options:
  -h, --help     Show this screen.
  -v, --version  Show version.

Available biobox types

  short_read_assembler  Assemble short reads into contigs
"""

from docopt  import docopt

def run():
    biobox = select_biobox(sys.argv[1:])

def select_biobox(argv):
    from version import __version__
    opts = docopt(__doc__,
                  argv          = argv,
                  version       = __version__,
                  options_first = True)

    biobox = get_biobox_module(opts['<biobox_type>'])
    return biobox

def get_biobox_module(name):
    key = ".".join(["biobox_cli", "type", name])
    return __import__(key)
