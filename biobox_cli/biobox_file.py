import os
import ruamel.yaml as yaml

def generate(args):
    output = {"version" : "0.9.0", "arguments" : args}
    return yaml.safe_dump(output, default_flow_style = False)

def get_biobox_file_contents(dir_):
    with open(os.path.join(dir_, 'biobox.yaml'), 'r') as f:
        return yaml.load(f.read())
