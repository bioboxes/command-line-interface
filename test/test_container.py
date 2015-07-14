import nose.tools           as nose
import biobox_cli.container as ctn

import helper as hlpr

def test_get_client():
    ctn.client()

def test_checking_a_local_available_image():
    nose.assert_equal(ctn.image_available_locally("python"), True)

def test_checking_an_local_available_image_with_tag():
    nose.assert_equal(ctn.image_available_locally("python:2.7"), True)

def test_checking_a_locally_non_existent_image():
    nose.assert_equal(ctn.image_available_locally("biobox/unknown"), False)

def test_checking_an_available_image():
    nose.assert_equal(ctn.image_available("python"), True)

def test_checking_an_available_image_with_tag():
    nose.assert_equal(ctn.image_available("python:2.7"), True)

def test_create_mount_string_with_relative_dir():
    expected = "{}/tmp:/tmp:ro".format(hlpr.project_root())
    nose.assert_equal(ctn.mount_string("tmp", "/tmp"), expected)

def test_create_mount_string_with_absolute_dir():
    expected = "/tmp:/tmp:ro"
    nose.assert_equal(ctn.mount_string("/tmp", "/tmp"), expected)

def test_create_output_mount_string():
    expected = "/tmp:/bbx/output:rw"
    nose.assert_equal(ctn.output_directory_mount_string("/tmp"), expected)

def test_create_output_mount_string():
    expected = "/tmp:/bbx/input:ro"
    nose.assert_equal(ctn.biobox_file_mount_string("/tmp"), expected)

def test_create_container_with_no_volumes():
    container = ctn.create("bioboxes/velvet", "default")
    attr = ctn.client().inspect_container(container)
    nose.assert_equal(attr["Volumes"], {})
    if not hlpr.is_ci_server():
        attr = ctn.client().remove_container(container)

def test_create_container_with_volumes():
    container = ctn.create("bioboxes/velvet", "default", ["/host:/cont:ro"])
    attr = ctn.client().inspect_container(container)
    nose.assert_in("/host", attr["Volumes"])
    if not hlpr.is_ci_server():
        attr = ctn.client().remove_container(container)
