"""
biobox - A command line interface for running biobox Docker containers

Usage:
    biobox <command> [<biobox_type> <image> <args>...]

Options:
  -h, --help     Show this screen.
  -v, --version  Show version.

Commands:
    run     Run a biobox Docker image with input parameters
    verify  Verify that a Docker image matches the given specification type

Biobox types:

  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util as util
import sys

def run():
    args = input_args()
    valid, command = select_command(args)
    if valid:
        command.run(args)
    else:
        util.err_exit(command)

def input_args():
    """
    Get CL args excluding those consisting of only whitespace
    """
    return filter(lambda x: len(x) > 0,
        map(lambda x: x.strip(), sys.argv[1:]))

def select_command(argv):
    """
    Select the command line interface module
    """
    opts = util.parse_docopt(__doc__, argv, True)
    mod_name = ".".join(["biobox_cli", "command", opts['<command>']])
    try:
        __import__(mod_name)
    except ImportError:
        msg = """\
Unknown command: "{}".
Run `biobox --help` for a list of available commands.
"""
        return False, msg.format(opts['<command>'])
    return True, sys.modules[mod_name]
