import logging
logging.getLogger("requests").setLevel(logging.WARNING)

def client():
    import docker
    from docker.utils import kwargs_from_env
    client = docker.Client(**kwargs_from_env(assert_hostname = False))
    return client

def get_image_tags(docker_dict):
    return reduce(lambda acc, x: acc + [x, x.split(":")[0]],
            docker_dict['RepoTags'], [])

def image_available_locally(image):
    image_tags = map(get_image_tags, client().images())
    images = set(reduce(lambda acc, x: acc + x, image_tags, []))
    return image in images

def image_available(image):
    from docker.errors import APIError
    if not image_available_locally(image):
        output = client().pull(image)
        if "error" in output:
            return False
    return True

def mount_string(host_dir, container_dir, read_only = True):
    import os
    access = "ro" if read_only else "rw"
    return ":".join([os.path.abspath(host_dir), container_dir, access])

