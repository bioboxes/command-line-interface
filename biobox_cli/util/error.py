import yaml, sys
import biobox_cli.util.assets as asset

def err_message(msg_key, locals_):
    errors = yaml.load(asset.get_asset_file_contents('error_messages.yml'))
    return errors[msg_key].format(**locals_)

def err_exit(msg_key, locals_):
    sys.stderr.write(err_message(msg_key, locals_))
    exit(1)
