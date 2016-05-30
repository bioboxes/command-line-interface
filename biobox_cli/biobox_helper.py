from abc import ABCMeta, abstractmethod
import biobox_cli.container   as ctn
import biobox_cli.util.misc   as util
import tempfile as tmp
import inspect
from fn import monad

class Biobox:
    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare_volumes(opts):
        pass

    @abstractmethod
    def after_run(self, host_dst_dir):
        pass

    def run(self, argv):
        doc = inspect.getdoc(inspect.getmodule(self))
        opts = util.parse_docopt(doc, argv, False)
        task        = opts['--task']
        image       = opts['<image>']
        output      = opts['--output']
        memory      = opts['--memory']
        cpuset      = opts['--cpuset']
        cpushares   = opts['--cpu-shares']
        host_dst_dir = tmp.mkdtemp()
        volumes = self.prepare_volumes(opts, host_dst_dir)
        ctn.exit_if_no_image_available(image)
        cpushares = monad.Option.from_call(lambda x: int(x),cpushares).get_or(None)
        ctnr = ctn.create(image, task, volumes, memory=memory, cpuset=cpuset, cpu_shares=cpushares)
        ctn.run(ctnr)
        self.after_run(output, host_dst_dir)
        return ctnr

    def remove(self, container):
            """
            Removes a container
            Note this method is not tested due to limitations of circle ci
            """
            ctn.remove(container)
