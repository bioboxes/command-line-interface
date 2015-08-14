from setuptools import setup, find_packages
import biobox_cli

setup(
    name                 = 'biobox-cli',
    version              = biobox_cli.__version__,
    description          = 'Run biobox Docker containers on the command line',
    author               = 'bioboxes',
    author_email         = 'mail@bioboxes.org',
    url                  = 'http://bioboxes.org',
    scripts              = ['bin/biobox'],
    install_requires     = open('requirements.txt').read().splitlines(),

    packages             = find_packages(),
    package_data         = {'': ['assets/*']},
    include_package_data = True,

    classifiers = [
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX'
    ],
)
