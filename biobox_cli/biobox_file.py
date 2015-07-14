import os

def generate(args):
    import yaml
    output = {"version" : "0.9.0", "arguments" : args}
    return yaml.safe_dump(output, default_flow_style = False)

def fastq_arguments(mount_directory, *args):
    values = map(lambda (i, (p, t)), : entry("fastq_" + str(i), os.path.join(mount_directory, p), t),
            enumerate(args))
    return {"fastq" : values}

def entry(id_, value, type_):
    return {"id" : id_, "value" : value, "type" : type_}

def create_biobox_directory(content):
    import tempfile as tmp
    dir_ = tmp.mkdtemp()
    with open(os.path.join(dir_, "biobox.yaml"), "w") as f:
        f.write(content)
    return dir_
