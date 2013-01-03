#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from distutils.core import setup

setup(
    name='rdlm',
    version='0.1a1',
    author="Fabien MARTY",
    author_email="fabien.marty@gmail.com",
    url="https://github.com/thefab/restful-distributed-lock-manager",
    packages=['rdlm',],
    license='MIT',
    description="RDLM (Restful Distributed Lock Manager) is a lock manager over HTTP build on Tornado",
    scripts=["rdlm-daemon.py"]
)