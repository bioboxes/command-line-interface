import nose.tools as nt

def get_stream(context, stream):
    nt.assert_in(stream, ['stderr', 'stdout'],
            "Unknown output stream {}".format(stream))
    return getattr(context.output, stream)

@when(u'I run the command')
def step_impl(context):
    context.output = context.env.run(context.text,
            expect_error  = True,
            expect_stderr = True)

@then(u'the {stream} should be empty')
def step_impl(context, stream):
    output = get_stream(context, stream)
    nt.assert_equal(output, "",
            "The {} should be empty but contains {}".format(stream, output))

@then(u'the exit code should be {code}')
def step_impl(context, code):
    returned = context.output.returncode
    nt.assert_equal(returned, int(code),
            "Process should return exit code {} but was {}".format(code, returned))

@then(u'the {stream} should contain')
def step_impl(context, stream):
    output = get_stream(context, stream)
    nt.assert_in(context.text, output)
