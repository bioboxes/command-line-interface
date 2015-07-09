import nose.tools           as nose
import biobox_cli.container as ctn

def test_get_client():
    ctn.client()

def test_checking_an_available_image():
    nose.assert_equal(ctn.image_available("python"), True)

def test_checking_an_available_image_with_tag():
    nose.assert_equal(ctn.image_available("python:2.7"), True)

def test_checking_an_non_existent_image():
    nose.assert_equal(ctn.image_available("biobox/unknown"), False)
