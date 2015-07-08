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

import biobox_cli.util as util
import sys

def run():
    args = sys.argv[1:]
    biobox = select_biobox(args)
    biobox.run(args)

def select_biobox(argv):
    opts = util.command_line_args(__doc__, argv, True)
    mod_name = ".".join(["biobox_cli", "type", opts['<biobox_type>']])
    __import__(mod_name)
    return sys.modules[mod_name]
