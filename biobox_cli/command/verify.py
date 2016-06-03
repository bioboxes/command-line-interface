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
  profiling_benchmark   Profiling benchmark tools
  assembler_benchmark   Assembler benchmrark tools
  assembler_read_based_benchmark   Assembler Read based Benchmark tools
  taxonomic_binning_benchmark   Taxonomic Binning Benchmark tools
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
        str.replace(str(name), "Should ", ""),
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
            F(map, lambda x: name_and_status(*x)),
            F(list)])
        longest_name = fn.thread([
            statuses,
            F(map, fn.first),
            F(map, len),
            max])
        def justify(x, y): return x.ljust(longest_name), y


        output = fn.thread([
            statuses,
            F(map, lambda x: justify(*x)),
            F(map, F("   ".join)),
            fn.unique,
            F("\n".join)])
        print(output)
    elif behave.is_failed(results):
        if log:
            sys.stderr = open(log, "w+")
        msg = fn.thread([
            behave.get_failing_scenarios(results),
            F(map, behave.scenario_name),
            F("\n".join)])

        error.err_exit('failed_verification', {'image': image, 'error': msg, 'biobox' : biobox})
