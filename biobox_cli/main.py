"""
biobox - A command line interface for running biobox Docker containers

Usage:
    biobox <biobox_type> <container> [<args>...]

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
    valid, biobox = select_biobox(args)
    if valid:
        biobox.run(args)
    else:
        sys.stderr.write(biobox)
        exit(1)

def select_biobox(argv):
    opts = util.command_line_args(__doc__, argv, True)
    mod_name = ".".join(["biobox_cli", "type", opts['<biobox_type>']])
    try:
        __import__(mod_name)
    except ImportError:
        msg = """\
Unknown biobox container type: "{}".
Run `biobox --help` for a list of available biobox types.
"""
        return False, msg.format(opts['<biobox_type>'])
    return True, sys.modules[mod_name]
