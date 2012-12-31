#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from tornado.options import define
from tornado.options import options as tornado_options

define("port", default=8888, type=int, metavar="PORT", help="main port (of the lock manager)", group="rdlm")

class Options(object):
    '''Class to store command line options'''

    @property
    def port(self):
        '''
        @summary: returns the main port of the daemon
        @result: the port of the daemon (as an integer)
        '''
        return tornado_options.port
