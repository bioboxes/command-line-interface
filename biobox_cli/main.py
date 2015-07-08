"""
biobox - A command line interface for running biobox Docker containers

Usage:
    biobox <box_type> <container> [options]

Options:
  -h, --help     Show this screen.
  -v, --version  Show version.
"""

from docopt  import docopt
from version import __version__ as version

def run():
    docopt(__doc__, version = version)
