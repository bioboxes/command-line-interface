import nose.tools                 as nose
import biobox_cli.util.functional as fn
import operator                   as op

from fn import F

def test_thread():
    args = [1, F(op.add, 2), F(op.mul, 3)]
    nose.assert_equal(9, fn.thread(args))
