#!/usr/bin/env python3
from setuptools import find_packages
from setuptools import setup

import challenger

setup(
    name='challenger',
    version=challenger.__version__,
    packages=find_packages()
)

# pylint: skip-file
