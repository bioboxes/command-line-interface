"""
biobox login - Log in to a biobox container with mounted test data

Usage:
    biobox login <biobox_type> <image> [<args>...]

Options:
  -h, --help     Show this screen.
  -r, --no-rm    Don't remove the container after the process finishes
  -t, --no-tty   Don't start a terminal emulator, used for scripted interactions.

Available Biobox types:
  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util.misc as util
import biobox_cli.container as docker


def run(argv):
    opts = util.parse_docopt(__doc__, argv, True)

    image  = opts["<image>"]
    tty    = not "--no-tty" in opts["<args>"]
    remove = not "--no-rm"  in opts["<args>"]

    ctnr = docker.create_tty(image, tty)
    docker.login(ctnr)

    #module = util.select_module("biobox_type", )
    #ctnr = module.login()

    if remove:
        docker.remove(ctnr)
