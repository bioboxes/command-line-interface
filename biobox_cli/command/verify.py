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
import biobox_cli.container        as ctn

def run(argv):
    opts   = util.parse_docopt(__doc__, argv, False)
    biobox = opts['<biobox_type>']
    image  = opts['<image>']
    task   = opts['--task']

    ctn.exit_if_no_image_available(image)

    results = behave.run(biobox, image, task)

    if behave.is_failed(results):
        error = "\n".join(map(behave.scenario_name, behave.get_failing(results)))
        util.err_exit('failed_verification', {'image': image, 'error': error, 'biobox' : biobox})
