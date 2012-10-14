#!/usr/bin/env python

from setuptools import setup, find_packages

import version

setup(
    name = "botrocketsdk",
    packages = ['brplatform',],
    version = version.VERSION,
    author = "Alan Illing",
    description = ("Testing and helper framework for the Bot Rocket cloud platform"),
    license = "GPL",
    url = "https://github.com/ailling/botrocketsdk",
    install_requires=['requests>=0.13.1',]
)
