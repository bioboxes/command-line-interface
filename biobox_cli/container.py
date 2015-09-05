import logging, os
logging.getLogger("requests").setLevel(logging.WARNING)

import docker
import docker.utils

import biobox_cli.util as util

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
        util.err_exit('unknown_image', {'image': image})

def mount_string(host_dir, container_dir, read_only = True):
    access = "ro" if read_only else "rw"
    return ":".join([os.path.abspath(host_dir), container_dir, access])

def output_directory_mount_string(directory):
    return mount_string(directory, "/bbx/output", False)

def biobox_file_mount_string(directory):
    return mount_string(directory, "/bbx/input")

def create(image, command, mounts = []):
    return client().create_container(
            image,
            command,
            volumes     = map(lambda x: x.split(":")[0], mounts),
            host_config = docker.utils.create_host_config(binds=mounts))

def run(container):
    client().start(container)
    client().wait(container)
