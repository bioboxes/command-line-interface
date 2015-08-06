"""
biobox - A command line interface for running biobox Docker containers

Usage:
    biobox <command> <biobox_type> <image> [<args>...]

Options:
  -h, --help       Show this screen.
  -v, --version    Show version.

Commands:
    run       Run a biobox Docker image with input parameters
    verify    Verify that a Docker image matches the given specification type

Biobox types:
    short_read_assembler    Assemble short reads into contigs
"""

import biobox_cli.util as util
import sys

def run():
    args = input_args()
    opts = util.parse_docopt(__doc__, args, True)
    util.select_module("command", opts["<command>"]).run(args)

def input_args():
    """
    Get CL args excluding those consisting of only whitespace
    """
    return filter(lambda x: len(x) > 0,
        map(lambda x: x.strip(), sys.argv[1:]))
