# !/usr/bin/env python
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="ermiaoweb",
    version="0.0.1",
    author="dinghai",
    author_email="dhairoot@126.com",
    description="tiny web framework",
    long_description=open("README.rst").read(),
    license="GPL",
    url="https://github.com/ding-hai/ErmiaoWeb",
    packages=['ermiaoweb'],
    install_requires=[
        "Jinja2",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: System :: Operating System Kernels :: Linux",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
    ],
)
