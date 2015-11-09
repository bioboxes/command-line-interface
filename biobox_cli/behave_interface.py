import tempfile, json, os
from os import path

from fn import F, _
import fn.iters

import biobox_cli.util.functional as fn


def feature_file(biobox):
    """
    Returns the fullpath for the corresponding feature file for the given biobox type.
    """
    from pkg_resources import resource_filename
    file_ = biobox + '.feature'
    return path.abspath(resource_filename(__name__, path.join('verification', file_)))

def features_available(biobox):
    """
    Returns True if a feature file is available for the given biobox type
    """
    return path.isfile(feature_file(biobox))

def tmp_feature_dir():
    """
    Returns the fullpath of a 'biobox_verify' directory created in the current
    working directory.
    """
    return path.abspath(path.join(os.getcwd(), 'biobox_verify'))

def run(biobox_type, image, task, stop = True):
    """
    Runs the behave cucumber features for the given biobox and tast given by
    the passed arguments. Creates a directory in the current working directory,
    where the verfication files are created. Returns a dictionary of the behave
    output.
    """
    from behave.__main__ import main as behave_main
    _, tmp_file = tempfile.mkstemp()

    cmd = "{file} --define IMAGE={image} --define TASK={task} --define TMPDIR={tmp_dir} --outfile {tmp_file} --format json.pretty --no-summary"
    if stop:
      cmd += " --stop"
    args = {'file':     feature_file(biobox_type),
            'tmp_dir':  tmp_feature_dir(),
            'image':    image,
            'tmp_file': tmp_file,
            'task':     task}

    behave_main(cmd.format(**args))

    with open(tmp_file, 'r') as f:
        return json.loads(f.read())

def is_failed(behave_data):
    """
    Parses a behave dictionary and returns true if any verifications have
    failed.
    """
    return "failed" in map(lambda i: i['status'], behave_data)

def get_scenarios(behave_data):
    acc = []
    for item in behave_data:
        acc += item['elements']
    return acc

def scenario_name(scenario):
    return scenario["name"]

def scenario_status(scenario):
    """
    Returns the status of the last step in a scenario
    """
    status = list(fn.thread([
        scenario['steps'],
        F(map, fn.get("result")),
        F(filter, fn.is_not_none),
        F(map, fn.get("status")),
        ]))
    if fn.is_empty(status):
        return "not run"
    else:
        return status[-1]

def is_failed_scenario(scenario):
    return scenario_status(scenario) == "failed"

def get_failing_scenarios(behave_data):
    """
    Returns all failing scenarios from a behave dictionary
    """
    return list(filter(is_failed_scenario, get_scenarios(behave_data)))

def get_scenarios_and_statuses(behave_data):
    """
    Returns a list of scenarios and their status
    """
    return list(fn.thread([
        get_scenarios(behave_data),
        F(map, lambda x: [scenario_name(x), scenario_status(x)])]))
