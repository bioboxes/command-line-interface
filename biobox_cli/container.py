import logging, os
logging.getLogger("requests").setLevel(logging.WARNING)

import biobox.util               as docker
import biobox.image.availability as avail
import biobox.image.volume       as vol

import biobox_cli.util.error as error
import dockerpty             as pty

def exit_if_no_image_available(image):
    from biobox.exception import NoImageFound
    try:
        avail.get_image(image)
    except NoImageFound:
        error.err_exit('unknown_image', {'image': image})

def create_tty(image, tty, volumes = []):
    command = ""
    return docker.client().create_container(
            image,
            command,
            stdin_open  = True,
            tty         = tty,
            entrypoint  = '/bin/bash',
            volumes     = list(map(vol.get_host_path, volumes)),
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
