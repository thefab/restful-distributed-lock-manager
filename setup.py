#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from distutils.core import setup

description = "RDLM (Restful Distributed Lock Manager) is a lock manager over HTTP build on Tornado"
try:
    with open('README.rst') as f:
        long_description = f.read()
except IOError:
    long_description = description

setup(
    name='rdlm',
    version='0.1a1',
    author="Fabien MARTY",
    author_email="fabien.marty@gmail.com",
    url="https://github.com/thefab/restful-distributed-lock-manager",
    packages=['rdlm',],
    license='MIT',
    download_url='https://github.com/thefab/restful-distributed-lock-manager',
    description=description,
    long_description=long_description,
    scripts=["rdlm-daemon.py"],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',    
        'Topic :: Utilities',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
      ]
)