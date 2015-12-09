import time, pexpect, re

PROMPT = "root@\w+:[^\r]+"
UP_ARROW  = "\x1b[A"

def type(process, input_):
    process.send(input_.encode())
    time.sleep(3)
    process.expect(PROMPT)
    # Remove the typed input from the returned standard out
    return re.sub(re.escape(input_.strip()), '', process.buffer).strip()

@when(u'I run the interactive command')
def step_impl(context):
    process = pexpect.spawn(context.text)
    time.sleep(3)

    class Output(object):
        pass

    context.output = Output()
    context.output.stderr = ""
    context.output.stdout = ""
    context.process = process

@when(u'I type')
def step_impl(context):
    cmd = context.text.strip() + "\n"
    context.output.stdout = type(context.process, cmd)

@when(u'I exit the shell')
def step_impl(context):
    context.process.send("exit\n")
