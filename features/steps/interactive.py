import os.path, sys, time
import nose.tools as nt

import subprocess as spr

@when(u'I run the interactive command')
def step_impl(context):
    cmd = context.text
    context.process = spr.Popen(
            cmd.split(' '),
            shell  = True,
            stdin  = spr.PIPE,
            stdout = spr.PIPE,
            stderr = spr.PIPE)

@when(u'I type')
def step_impl(context):
    class Output(object):
        pass
    context.output = Output()
    context.output.stdout, context.output.stderr = context.process.communicate(input = context.text.encode())
