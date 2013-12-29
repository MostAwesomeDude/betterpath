#!/usr/bin/env python

from setuptools import setup

setup(
    name="betterpath",
    packages=["bp", "bp.tests"],
    setup_requires=["vcversioner"],
    vcversioner={},
    install_requires=open("requirements.txt").read().split("\n"),
    author="Corbin Simpson",
    author_email="cds@corbinsimpson.com",
    description="Path manipulation library",
    long_description=open("README.rst").read(),
    license="MIT/X11",
    url="http://github.com/MostAwesomeDude/betterpath",
)
