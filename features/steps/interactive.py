import time, pexpect, re
import nose.tools as nt
import subprocess as spr

PROMPT   = "root@\w+:[^\r]+"
UP_ARROW = "\x1b[A"

def type(process, input_):
    process.send(input_.encode())
    process.expect(PROMPT)
    # Remove the typed input from the returned standard out
    return re.sub(re.escape(input_.strip()), '', process.before).strip()

@when(u'I run the interactive command')
def step_impl(context):
    process = pexpect.spawn(context.text)
    time.sleep(0.5)

    type(process, UP_ARROW)

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
