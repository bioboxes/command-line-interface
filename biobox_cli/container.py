import logging, os
logging.getLogger("requests").setLevel(logging.WARNING)
try:
    from functools import reduce
except ImportError:
    pass

import biobox.util               as docker
import biobox.image.availability as avail
from biobox.exception import NoImageFound

import biobox_cli.util.error as error
import dockerpty             as pty

def exit_if_no_image_available(image):
    try:
        avail.get_image(image)
    except NoImageFound:
        error.err_exit('unknown_image', {'image': image})

def create(image, command, volumes = [], memory = None, cpu_shares = None, cpuset = None):
    return docker.client().create_container(
            image,
            command,
            cpu_shares = cpu_shares,
            cpuset = cpuset,
            volumes     = list(map(lambda x: x.split(":")[0], volumes)),
            host_config = docker.client().create_host_config(binds=volumes, mem_limit=memory))

def create_tty(image, tty, volumes = []):
    command = ""
    return docker.client().create_container(
            image,
            command,
            stdin_open  = True,
            tty         = tty,
            entrypoint  = '/bin/bash',
            volumes     = list(map(lambda x: x.split(":")[0], volumes)),
            host_config = docker.client().create_host_config(binds=volumes))

def run(container):
    docker.client().start(container)
    docker.client().wait(container)

def login(container):
    docker.client().start(container)
    pty.PseudoTerminal(docker.client(), container).start()
    docker.client().stop(container)

def remove(container):
    """
    Removal of a container
    NOTE: This method is not tested due to circle ci limitations
    """
    docker.client().remove_container(container, v=True)
