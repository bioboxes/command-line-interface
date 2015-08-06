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

def run(argv):
    opts = util.parse_docopt(__doc__, argv, False)
    util.select_module("biobox_type", opts["<biobox_type>"]).run(argv)
