"""
biobox verify - Verify that a Docker image matches the given specification type

Usage:
    biobox verify <biobox_type> <image> [--task=TASK] [--verbose] [--log=FILE]

Options:
  -h, --help             Show this screen.
  -t TASK, --task=TASK   Specify which biobox task to test. [default: default]
  -v, --verbose          Show the status of each biobox verification test.
  -l FILE, --log=FILE    Log test results to file.

Available Biobox types:

  short_read_assembler  Assemble short reads into contigs
"""
from __future__ import print_function

import biobox_cli.util.misc        as util
import biobox_cli.util.error       as error
import biobox_cli.util.functional  as fn
import biobox_cli.behave_interface as behave
import biobox_cli.container        as ctn

import string
import sys

from fn    import F, _
from fn.op import flip

def name_and_status(x, y):
    return format_scenario_name(x), format_scenario_status(y)

def format_scenario_name(name):
    return fn.thread([
        str.replace(name, "Should ", ""),
        lambda x: x[0].upper() + x[1:],
        F(flip(str.split), '--'),
        fn.first,
        str.strip])

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
    log     = opts['--log']

    if not behave.features_available(biobox):
        error.err_exit("unknown_command",
                {"command_type" : "biobox type", "command" : biobox})

    ctn.exit_if_no_image_available(image)

    if verbose:
        results = behave.run(biobox, image, task, False)
    else:
        results = behave.run(biobox, image, task)

    if verbose:
        if log:
            sys.stdout = open(log, "w+")
        statuses = fn.thread([
            behave.get_scenarios_and_statuses(results),
            F(map, name_and_status)])
        longest_name = fn.thread([
            statuses,
            F(map, fn.first),
            F(map, len),
            max])
        def justify(x, y): return string.ljust(x, longest_name, ' '), y
        output = fn.thread([
            statuses,
            F(map, justify),
            F(map, F(flip(string.join), "   ")),
            fn.unique,
            F(flip(string.join), "\n")])
        print(output)
    elif behave.is_failed(results):
        if log:
            sys.stderr = open(log, "w+")
        msg = fn.thread([
            behave.get_failing_scenarios(results),
            F(map, behave.scenario_name),
            F(flip(string.join), "\n")])

        error.err_exit('failed_verification', {'image': image, 'error': msg, 'biobox' : biobox})
