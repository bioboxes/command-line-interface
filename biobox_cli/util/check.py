import os

def is_a_valid_file(path):
    from biobox_cli.exception import InputFileNotFound
    full_path = os.path.abspath(path)
    if not os.path.isfile(full_path):
        msg = "Given input file does not exist: {}"
        raise InputFileNotFound(msg.format(full_path))
