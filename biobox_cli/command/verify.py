"""
biobox verify - Verify that a Docker image matches the given specification type

Usage:
    biobox verify <biobox_type> <image> [--task=TASK]

Options:
  -h, --help             Show this screen.
  -t TASK --task=TASK    Specify which biobox task to test. [default: default]

Available Biobox types:

  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util             as util
import biobox_cli.behave_interface as behave

def run(argv):
    opts   = util.parse_docopt(__doc__, argv, False)
    biobox = opts['<biobox_type>']
    image  = opts['<image>']
    task   = opts['--task']

    results = behave.run(biobox, image, task)

    if "failed" in map(lambda i: i['status'], results):
        util.err_exit('failed_verification', {'image': image, 'biobox': biobox.replace('_', ' ')})
