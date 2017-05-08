from biobox.exception import BioboxesException

class InputFileNotFound(BioboxesException):
    """
    An input file given to the CLI does not exist.
    """
