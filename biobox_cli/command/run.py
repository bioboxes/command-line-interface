"""
biobox run - Run a biobox Docker image with input parameters

Usage:
    biobox run <biobox_type> <image> [<args>...]

Options:
  -h, --help     Show this screen.
  -r, --no-rm    Don't remove the container after the process finishes

Available Biobox types:
  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util.misc as util
from biobox_cli.biobox_helper import Biobox as ABiobox

def run(argv):
    opts = util.parse_docopt(__doc__, argv, True)
    module = util.select_module("biobox_type", opts["<biobox_type>"])
    Biobox = next(util.get_subclasses(module, ABiobox))
    bbx = Biobox()
    ctnr = bbx.run(argv)
    if not '--no-rm' in argv:
        bbx.remove(ctnr)
