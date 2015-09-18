import os.path, sys, time
import nose.tools as nt

import subprocess as spr

import pexpect, re

PROMPT = 'root@\w+:[^\r]+'

@when(u'I run the interactive command')
def step_impl(context):
    process = pexpect.spawn(context.text)
    time.sleep(0.5)
    process.send(b"\x1b[A")
    process.expect(PROMPT)

    class Output(object):
        pass

    context.output = Output()
    context.output.stderr = ""
    context.output.stdout = ""

    context.process = process


@when(u'I type')
def step_impl(context):
    cmd = context.text.strip()
    context.process.sendline(cmd)
    context.process.expect(PROMPT)
    context.output.stdout = re.sub(re.escape(cmd),
                                   '',
                                   context.process.before).strip()
