import logging, os
logging.getLogger("requests").setLevel(logging.WARNING)

import docker
import docker.utils

import biobox_cli.util.error as error
import dockerpty             as pty

def client():
    client = docker.Client(**docker.utils.kwargs_from_env(assert_hostname = False))
    return client

def get_image_tags(docker_dict):
    return reduce(lambda acc, x: acc + [x, x.split(":")[0]],
            docker_dict['RepoTags'], [])

def is_image_available_locally(image):
    image_tags = map(get_image_tags, client().images())
    images = set(reduce(lambda acc, x: acc + x, image_tags, []))
    return image in images

def is_image_available(image):
    if not is_image_available_locally(image):
        output = client().pull(image)
        if "error" in output:
            return False
    return True

def exit_if_no_image_available(image):
    if not is_image_available(image):
        error.err_exit('unknown_image', {'image': image})

def volume_string(host_dir, container_dir, read_only = True):
    access = "ro" if read_only else "rw"
    return ":".join([os.path.abspath(host_dir), container_dir, access])

def output_directory_volume_string(directory):
    return volume_string(directory, "/bbx/output", False)

def input_directory_volume_string(directory):
    return volume_string(directory, "/bbx/input", True)

def biobox_file_volume_string(directory):
    return volume_string(directory, "/bbx/input")

def create(image, command, volumes = []):
    return client().create_container(
            image,
            command,
            volumes     = map(lambda x: x.split(":")[0], volumes),
            host_config = docker.utils.create_host_config(binds=volumes))

def create_tty(image, tty, volumes = []):
    command = ""
    return client().create_container(
            image,
            command,
            stdin_open  = True,
            tty         = tty,
            entrypoint  = '/bin/bash',
            volumes     = map(lambda x: x.split(":")[0], volumes),
            host_config = docker.utils.create_host_config(binds=volumes))

def run(container):
    client().start(container)
    client().wait(container)

def login(container):
    client().start(container)
    pty.PseudoTerminal(client(), container).start()
    client().stop(container)

def remove(container):
    """
    Removal of a container
    NOTE: This method is not tested due to circle ci limitations
    """
    client().remove_container(container, v=True)
