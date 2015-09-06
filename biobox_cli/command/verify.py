"""
biobox verify - Verify that a Docker image matches the given specification type

Usage:
    biobox verify <biobox_type> <image> [--task=TASK] [--verbose]

Options:
  -h, --help             Show this screen.
  -t TASK, --task=TASK   Specify which biobox task to test. [default: default]
  -V, --verbose          Show the status of each biobox verification test.

Available Biobox types:

  short_read_assembler  Assemble short reads into contigs
"""

import biobox_cli.util.misc        as util
import biobox_cli.util.error       as error
import biobox_cli.util.functional  as fn
import biobox_cli.behave_interface as behave
import biobox_cli.container        as ctn

import string

from fn    import F, _
from fn.op import flip

def format_scenario_name(name):
    return fn.thread([
        string.replace(name, "Should ", ""),
        lambda x: x[0].upper() + x[1:],
        F(flip(string.split), '--'),
        fn.first,
        string.strip])

def format_scenario_status(status):
    formats = {
            'passed'  : 'PASS',
            'failed'  : 'FAIL',
            'not run' : 'NOT RUN'}
    return formats[status]

def run(argv):
    opts    = util.parse_docopt(__doc__, argv, False)
    biobox  = opts['<biobox_type>']
    image   = opts['<image>']
    task    = opts['--task']
    verbose = opts['--verbose']

    ctn.exit_if_no_image_available(image)

    results = behave.run(biobox, image, task)

    if verbose:
        statuses = fn.thread([
            behave.get_scenarios_and_statuses(results),
            F(map, lambda (x, y): (format_scenario_name(x), format_scenario_status(y)))])
        longest_name = fn.thread([
            statuses,
            F(map, fn.first),
            F(map, len),
            max])
        output = fn.thread([
            statuses,
            F(map, lambda (x, y): (string.ljust(x, longest_name, ' '), y)),
            F(map, F(flip(string.join), "   ")),
            fn.unique,
            F(flip(string.join), "\n")])
        print output
    elif behave.is_failed(results):
        msg = fn.thread([
            behave.get_failing_scenarios(results),
            F(map, behave.scenario_name),
            F(flip(string.join), "\n")])

        error.err_exit('failed_verification', {'image': image, 'error': msg, 'biobox' : biobox})
