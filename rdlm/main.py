#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

import tornado.ioloop
import tornado.web
from rdlm.options import Options 
from rdlm.hello_handler import HelloHandler
from rdlm.active_locks_handler import ActiveLocksHandler
from rdlm.locks_handler import LocksHandler
from rdlm.unit_testing import UnitTestingHandler
from rdlm.lock import LOCK_MANAGER_INSTANCE

def on_every_second():
    '''
    @summary: function called by tornado/ioloop every second
    
    It's used to clear expired locks
    '''
    LOCK_MANAGER_INSTANCE.clean_expired_locks()

def get_app(unit_testing = False):
    '''
    @summary: returns the tornado application
    @param unit_testing: if True, we add some handler for unit testing only
    @result: the tornado application
    '''
    url_list = [
        tornado.web.URLSpec(r"/", HelloHandler, name="hello"),
        tornado.web.URLSpec(r"/active_locks/([a-zA-Z0-9]+)", ActiveLocksHandler, name="active_locks"),
        tornado.web.URLSpec(r"/locks/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)", LocksHandler, name="lock")
    ]
    if unit_testing:
        url_list.append(tornado.web.URLSpec(r"/reset", UnitTestingHandler, name="unit_testing"))
    application = tornado.web.Application(url_list)
    return application

def get_ioloop():
    iol = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(on_every_second, 1000, iol).start()
    return iol

def main():
    '''
    @summary: main function (starts the daemon)
    '''
    application = get_app()
    tornado.options.parse_command_line()
    application.listen(Options().port)
    iol = get_ioloop()
    iol.start()
