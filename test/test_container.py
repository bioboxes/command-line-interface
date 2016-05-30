import nose.tools           as nose
import biobox_cli.container as ctn

import biobox.util as docker

import helper as hlpr

def test_create_volume_string_with_relative_dir():
    expected = "{}/tmp:/tmp:ro".format(hlpr.project_root())
    nose.assert_equal(ctn.volume_string("tmp", "/tmp"), expected)

def test_create_volume_string_with_absolute_dir():
    expected = "/tmp:/tmp:ro"
    nose.assert_equal(ctn.volume_string("/tmp", "/tmp"), expected)

def test_create_output_volume_string():
    expected = "/tmp:/bbx/output:rw"
    nose.assert_equal(ctn.output_directory_volume_string("/tmp"), expected)

def test_create_output_volume_string():
    expected = "/tmp:/bbx/input:ro"
    nose.assert_equal(ctn.biobox_file_volume_string("/tmp"), expected)

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
