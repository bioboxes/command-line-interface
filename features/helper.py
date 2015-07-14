import os
import nose.tools as nt

def get_stream(context, stream):
    nt.assert_in(stream, ['stderr', 'stdout'],
            "Unknown output stream {}".format(stream))
    return getattr(context.output, stream)

def get_file_path(context, file_):
    return os.path.join(context.env.cwd, file_)
