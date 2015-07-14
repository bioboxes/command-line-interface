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
