import os
import yaml

def generate(args):
    output = {"version" : "0.9.0", "arguments" : args}
    return yaml.safe_dump(output, default_flow_style = False)

def parse(dir_):
    with open(os.path.join(dir_, 'biobox.yaml'), 'r') as f:
        return yaml.load(f.read())

def fastq_arguments(args):
    return files_values("fastq", args)

def fasta_arguments(args):
    return files_values("fasta", args)

def reference_argument(ref):
    return {"fasta_dir": ref}

def files_values(identifier, args):
    values = [entry(identifier + "_" + str(i), p_c, t) for (i, (p_c, t)) in enumerate(args)]
    return {identifier : values}

def entry(id_, value, type_):
    return {"id" : id_, "value" : value, "type" : type_}

def create_biobox_directory(content):
    import tempfile as tmp
    dir_ = tmp.mkdtemp()
    with open(os.path.join(dir_, "biobox.yaml"), "w") as f:
        f.write(content)
    return dir_
