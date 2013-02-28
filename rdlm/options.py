#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from tornado.options import define
from tornado.options import options as tornado_options

define("port", default=8888, type=int, metavar="PORT",
       help="main port (of the lock manager)", group="rdlm")
define("admin_userpass_file", default="yes", type=str, metavar="ADMIN_USERPASS_FILE",
       help="the full path of an admin userpass file (special values : no => no admin requests, \
             yes => no auth for admin requests)", group="rdlm")


class Options(object):
    '''Class to store command line options'''

    @classmethod
    def port(cls):
        '''
        @summary: returns the main port of the daemon
        @result: the port of the daemon (as an integer)
        '''
        return tornado_options.port

    @classmethod
    def admin_userpass_file(cls):
        '''
        @summary: returns the admin userpass file
        @result: the full path of the admin userpass file
        '''
        return tornado_options.admin_userpass_file
