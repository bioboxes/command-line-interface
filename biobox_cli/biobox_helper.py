import tempfile, inspect
from abc import ABCMeta, abstractmethod
from fn import monad

import biobox.image.execute as biobox
import biobox_cli.container as ctn
import biobox_cli.util.misc as util

def int_or_none(c):
    return monad.Option.from_call(lambda x: int(x), c).get_or(None)

class Biobox:
    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare_config(self, opts):
        pass

    @abstractmethod
    def after_run(self, host_dst_dir):
        pass

    @abstractmethod
    def get_version(self):
        pass

    def run(self, argv):
        doc = inspect.getdoc(inspect.getmodule(self))
        opts = util.parse_docopt(doc, argv, False)
        task        = opts['--task']
        image       = opts['<image>']
        output      = opts['--output']

        # Check the image exists
        ctn.exit_if_no_image_available(image)

        # Additional non-biobox args to pass to the docker daemon
        docker_args = {'mem_limit': opts['--memory'],
                       'cpuset': opts['--cpuset'],
                       'cpu_shares': int_or_none(opts['--cpu-shares'])}

        output_dir = tempfile.mkdtemp()
        dirs = {"output": output_dir}

        config = self.prepare_config(opts)
        ctnr = biobox.create_container(image, config, dirs, task, self.get_version(), docker_args)
        ctn.run(ctnr)
        self.after_run(output, output_dir)
        return ctnr
