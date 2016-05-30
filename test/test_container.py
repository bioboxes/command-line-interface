import nose.tools           as nose
import biobox_cli.container as ctn

import biobox.util as docker

import helper as hlpr

def test_create_container_with_no_volumes():
    container = ctn.create("bioboxes/velvet", command="default")
    attr = docker.client().inspect_container(container)
    nose.assert_equal(attr["Config"]["Volumes"], None)
    hlpr.remove_container(container)

def test_create_container_with_volumes():
    container = ctn.create("bioboxes/velvet", command="default", volumes=["/host:/cont:ro"])
    attr = docker.client().inspect_container(container)
    nose.assert_in("/host", attr["Config"]["Volumes"])
    hlpr.remove_container(container)
