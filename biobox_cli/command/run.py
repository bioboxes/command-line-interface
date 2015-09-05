"""
biobox run - Run a biobox Docker image with input parameters

Usage:
    biobox run <biobox_type> <image> [<args>...]

Options:
  -h, --help     Show this screen.

Available Biobox types:
  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util as util

def run(argv):
    opts = util.parse_docopt(__doc__, argv, True)
    module = util.select_module("biobox_type", opts["<biobox_type>"])
    ctnr = module.run(argv)
    if not '--no-rm-container' in argv:
        module.remove(ctnr)