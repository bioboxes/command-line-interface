import pkg_resources, os, pkgutil
from setuptools import setup, find_packages
import biobox_cli

def dependencies():
    file_ = pkg_resources.resource_filename(__name__, os.path.join('requirements', 'default.txt'))
    with open(file_, 'r') as f:
        return f.read().splitlines()

setup(
    name                 = 'biobox-cli',
    version              = biobox_cli.__version__,
    description          = 'Run biobox Docker containers on the command line',
    author               = 'bioboxes',
    author_email         = 'mail@bioboxes.org',
    url                  = 'http://bioboxes.org',
    scripts              = ['bin/biobox'],
    install_requires     = dependencies(),

    packages             = find_packages(),
    package_data         = {'': ['assets/*']},
    include_package_data = True,

    classifiers = [
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX'
    ],
)
