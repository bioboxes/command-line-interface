"""
biobox login - Log in to a biobox container with mounted test data

Usage:
    biobox login <biobox_type> <image> [<args>...]

Options:
  -h, --help     Show this screen.
  -r, --no-rm    Don't remove the container after the process finishes
  -t, --no-tty   Don't start a terminal emulator, used for scripted interactions.

Available Biobox types:
  short_read_assembler  Assemble short reads into contigs
"""

import yaml

import biobox_cli.util.misc   as util
import biobox_cli.util.assets as asset
import biobox_cli.util.error  as error
import biobox_cli.container   as docker

def get_login_parameters(biobox_type):
    """
    Determines if the biobox type is currently supported for login. Returns
    a list of parameters for mounting data if it is.
    """
    params = yaml.load(asset.get_asset_file_contents('login_parameters.yml'))
    if biobox_type not in params:
        return None
    else:
        return params[biobox_type]


def create_login_file(dir_, params):
    from os.path import join
    from shutil  import copyfile

    is_literal = params['type'] == 'literal'
    dst = join(dir_, params['dst'])

    if is_literal:
        with open(dst, 'w') as f:
            f.write(params['src'])
    else:
        src = asset.get_data_file_path(params['src'])
        copyfile(src, dst)


def run(argv):
    opts = util.parse_docopt(__doc__, argv, True)

    image       = opts["<image>"]
    biobox_type = opts["<biobox_type>"]
    tty         = not "--no-tty" in opts["<args>"]
    remove      = not "--no-rm"  in opts["<args>"]

    params = get_login_parameters(biobox_type)
    if params is None:
        error.err_exit("unknown_command",
                {"command_type" : "biobox type", "command" : biobox_type})

    docker.exit_if_no_image_available(image)

    ctnr = docker.create_tty(image, tty)
    docker.login(ctnr)

    if remove:
        docker.remove(ctnr)
