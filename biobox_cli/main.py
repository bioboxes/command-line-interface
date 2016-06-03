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
    login     Log in to a biobox container with mounted test data

Biobox types:
    short_read_assembler    Assemble short reads into contigs
"""

import sys

from fn import F

import biobox_cli.util.misc       as util
import biobox_cli.util.functional as fn

def run():
    args = input_args()
    opts = util.parse_docopt(__doc__, args, True)
    util.select_module("command", opts["<command>"]).run(args)

def input_args():
    """
    Get command line args excluding those consisting of only whitespace
    """
    return fn.thread([
        sys.argv[1:],
        F(map, str.strip),
        F(filter, fn.is_not_empty),
        F(list)])
