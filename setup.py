#!/usr/bin/env python3

"""Setup and configuration."""

import os
from setuptools import setup
from setuptools import find_packages


NAME = 'evebot'
PWD = os.path.abspath(os.path.dirname(__name__))

METADATA_FILE = os.path.join(PWD, NAME, '__init__.py')
METADATA = {}
with open(METADATA_FILE) as init_file:
    exec(init_file.read(), METADATA)

REQUIREMENTS_FILE = os.path.join(PWD, 'requirements.txt')
REQUIREMENTS = []

with open(REQUIREMENTS_FILE) as req_file:
    REQUIREMENTS = req_file.read().splitlines()

setup(
    name=NAME,
    version=METADATA['__version__'],
    description=METADATA['__description__'],
    author=METADATA['__description__'],
    author_email=METADATA['__author_email__'],
    url=METADATA['__url__'],
    license=METADATA['__license__'],
    packages=find_packages('.'),
    install_requires=REQUIREMENTS,
    zip_safe=True,
    entry_points={
        'console_scripts': ['evebot=evebot.evebot:run',
                            'eveimport=evebot.utility.__main__:run',
                            'testcommand=evebot.commands.__main__:run']
    },
    classifiers=(
        'Development Status :: 5 - Production',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment',
    )
)
