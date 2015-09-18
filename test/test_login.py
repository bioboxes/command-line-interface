import nose.tools               as nose
import biobox_cli.command.login as login
import helper                   as hlpr

def test_get_login_parameters_with_unknown_type():
    nose.assert_equal(None, login.get_login_parameters('unknown'))
