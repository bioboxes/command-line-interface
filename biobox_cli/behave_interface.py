import tempfile, json, os
from os import path

import itertools as it
import functools as func

def behave_feature_file(biobox):
    from pkg_resources import resource_filename
    file_ = biobox + '.feature'
    return path.abspath(resource_filename(__name__, path.join('verification', file_)))

def tmp_feature_dir():
    return path.abspath(path.join(os.getcwd(), 'biobox_verify'))

def run(biobox_type, image, task):
    from behave.__main__ import main as behave_main
    _, tmp_file = tempfile.mkstemp()

    cmd = "{file} --define IMAGE={image} --define TASK={task} --define TMPDIR={tmp_dir} --outfile {tmp_file} --format json.pretty --no-summary --stop"
    args = {'file':     behave_feature_file(biobox_type),
            'tmp_dir':  tmp_feature_dir(),
            'image':    image,
            'tmp_file': tmp_file,
            'task':     task}

    behave_main(cmd.format(**args))

    with open(tmp_file, 'r') as f:
        return json.loads(f.read())

def is_failed(results):
    return "failed" in map(lambda i: i['status'], results)

def get(key):
    def _get(_dict):
        if key in _dict:
            return _dict[key]
        else:
            return None
    return _get

def is_not_none(i):
    return (i is not None)

def is_failed_scenario(scenario):
    return is_failed(filter(is_not_none, (map(get("result"), scenario['steps']))))

def get_failing(results):
    def f(acc, item):
        return acc + filter(is_failed_scenario, item['elements'])
    return reduce(f, results, [])

def scenario_name(scenario):
    return scenario["name"]
