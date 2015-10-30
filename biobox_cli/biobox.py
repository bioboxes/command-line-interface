from abc import ABCMeta, abstractmethod
import biobox_cli.container   as ctn
import biobox_cli.util.misc   as util
import tempfile as tmp

class Biobox:
    __metaclass__ = ABCMeta

    @abstractmethod
    def prepare_volumes(opts):
        pass

    @abstractmethod
    def get_doc(self):
        pass

    @abstractmethod
    def after_run(self, host_dst_dir):
        pass

    def run(self, argv):
        opts = util.parse_docopt(self.get_doc(), argv, False)
        task        = opts['--task']
        image       = opts['<image>']
        output      = opts['--output']
        host_dst_dir = tmp.mkdtemp()
        volumes = self.prepare_volumes(opts, host_dst_dir)
        ctn.exit_if_no_image_available(image)
        ctnr = ctn.create(image, task, volumes)
        ctn.run(ctnr)
        self.after_run(output, host_dst_dir)
        return ctnr

    def remove(self, container):
            """
            Removes a container
            Note this method is not tested due to limitations of circle ci
            """
            ctn.remove(container)