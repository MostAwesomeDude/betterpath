#!/usr/bin/env python
# Copyright (C) 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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
