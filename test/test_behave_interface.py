import nose.tools                  as nt
import biobox_cli.behave_interface as behave

def test_get_failing_for_single_pass():
    passing = {"keyword" : "Scenario",
                "name"    : "scenario name",
                "steps"   : [{'result' : {'status' : 'passed'}}]} 
    result = [{'status'   : 'passed',
               'elements' : [passing]}]
    nt.assert_equal([], behave.get_failing(result))

def test_get_failing_for_single_failure():
    scenario = {"keyword" : "Scenario",
                "name"    : "scenario name",
                "steps"   : [{'result' : {'status' : 'failed'}}]} 
    result = [{'status'   : 'failed',
               'elements' : [scenario]}]
    nt.assert_equal([scenario], behave.get_failing(result))

def test_get_failing_for_pass_and_failure():
    passing = {"keyword" : "Scenario",
                "name"    : "scenario name",
                "steps"   : [{'result' : {'status' : 'passed'}}]} 
    failing = {"keyword" : "Scenario",
                "name"    : "scenario name",
                "steps"   : [{'result' : {'status' : 'failed'}}]} 
    result = [{'status'   : 'failed',
               'elements' : [failing, passing]}]
    nt.assert_equal([failing], behave.get_failing(result))
