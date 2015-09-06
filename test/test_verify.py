import nose.tools                as nose
import biobox_cli.command.verify as verify

def test_format_scenario_name_with_simple_scenario():
    input_ = 'Should return an error when the biobox.yaml is missing the "arguments" field.'
    expect = 'Return an error when the biobox.yaml is missing the "arguments" field.'
    nose.assert_equal(verify.format_scenario_name(input_), expect)

def test_format_scenario_name_with_outline_scenario():
    input_ = 'Should return an error the biobox.yaml has an unknown additional field. -- @1.1'
    expect = 'Return an error the biobox.yaml has an unknown additional field.'
    nose.assert_equal(verify.format_scenario_name(input_), expect)
