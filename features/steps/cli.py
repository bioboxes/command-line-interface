import nose.tools as nt
import helper     as hp

@when(u'I run the command')
def step_impl(context):
    context.output = context.env.run(context.text,
            expect_error  = True,
            expect_stderr = True)

@then(u'the {stream} should be empty')
def step_impl(context, stream):
    output = hp.get_stream(context, stream)
    nt.assert_equal(output, "",
            "The {} should be empty but contains:\n\n{}".format(stream, output))

@then(u'the exit code should be {code}')
def step_impl(context, code):
    returned = context.output.returncode
    nt.assert_equal(returned, int(code),
            "Process should return exit code {} but was {}".format(code, returned))

@then(u'the {stream} should contain')
def step_impl(context, stream):
    output = hp.get_stream(context, stream)
    nt.assert_in(context.text, output)

@then(u'the {stream} should equal')
def step_impl(context, stream):
    output = hp.get_stream(context, stream)
    nt.assert_equal(context.text, output)

@then(u'the file "{}" should exist')
def step_impl(context, file_):
    nt.assert_true(os.path.isfile(hp.get_file_path(context, file_)),
            "The file \"{}\" does not exist.".format(file_))

@then(u'the file "{}" should not be empty')
def step_impl(context, file_):
    with open(hp.get_file_path(context, file_), 'r') as f:
        nt.assert_not_equal(f.read().strip(), "")
