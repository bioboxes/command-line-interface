import nose.tools                  as nt
import biobox_cli.behave_interface as behave

def feature(statuses):
    feature_state = "failed" if ("failed" in statuses) else "passing"
    return {'status'   : feature_state,
            'elements' : map(scenario, statuses)}

def scenario(status = "failed", name = "scenario name"):
    scen = {"keyword" : "Scenario", "name" : name, "steps" : [{}]}
    if status in ["failed", "passing"]:
        scen["steps"] = [{'result' : {'status' : status}}]
    return scen

def test_get_failing_scenarios_for_single_pass():
    features = [feature(["passing"])]
    nt.assert_equal([], behave.get_failing_scenarios(features))

def test_get_failing_scenarios_for_single_failure():
    features = [feature(["failed"])]
    nt.assert_equal([scenario()], behave.get_failing_scenarios(features))

def test_get_failing_scenarios_for_pass_and_failure():
    features = [feature(["failed", "passing"])]
    nt.assert_equal([scenario()], behave.get_failing_scenarios(features))

def test_get_failing_scenarios_for_multiple_failing_scenarios():
    features = [feature(["failed", "passing"]),
                feature(["failed", "passing"])]
    nt.assert_equal([scenario(), scenario()], behave.get_failing_scenarios(features))

def test_get_failing_scenarios_with_unrun_scenarios():
    features = [feature(["passing", "failed", "not-run"])]
    nt.assert_equal([scenario()], behave.get_failing_scenarios(features))

def test_get_scenarios_and_status():
    features = [feature(["failed", "passing"]),
                feature(["failed", "passing"])]
    expected = [["scenario name", "failed"],
                ["scenario name", "passing"],
                ["scenario name", "failed"],
                ["scenario name", "passing"]]
    nt.assert_equal(expected, behave.get_scenarios_and_statuses(features))

def test_scenario_name():
    nt.assert_equal("a", behave.scenario_name(scenario("failed", "a")))
    nt.assert_equal("b", behave.scenario_name(scenario("passing", "b")))
