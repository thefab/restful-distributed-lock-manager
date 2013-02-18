#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

import tornado.ioloop
import tornado.web
import logging

from rdlm.options import Options 
from rdlm.hello_handler import HelloHandler
from rdlm.locks_handler import LocksHandler
from rdlm.lock_handler import LockHandler
from rdlm.resource_handler import ResourceHandler
from rdlm.resources_handler import ResourcesHandler
from rdlm.lock import LOCK_MANAGER_INSTANCE

def on_every_second():
    '''
    @summary: function called by tornado/ioloop every second
    
    It's used to clear expired locks
    '''
    LOCK_MANAGER_INSTANCE.clean_expired_locks()

def get_app():
    '''
    @summary: returns the tornado application
    @param unit_testing: if True, we add some handler for unit testing only
    @result: the tornado application
    '''
    url_list = [
        tornado.web.URLSpec(r"/", HelloHandler, name="hello"),
        tornado.web.URLSpec(r"/resources/([a-zA-Z0-9]+)", ResourceHandler, name="resource"),
        tornado.web.URLSpec(r"/resources", ResourcesHandler, name="resources"),
        tornado.web.URLSpec(r"/locks/([a-zA-Z0-9]+)", LocksHandler, name="locks"),
        tornado.web.URLSpec(r"/locks/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)", LockHandler, name="lock")
    ]
    application = tornado.web.Application(url_list)
    return application

def get_ioloop():
    '''
    @summary: returns a configured tornado ioloop
    '''
    iol = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(on_every_second, 1000, iol).start()
    return iol

def log_is_ready():
    '''
    @summary: simple callback just to log that the daemon is ready
    '''
    logging.info("RDLM daemon is ready !")

def main():
    '''
    @summary: main function (starts the daemon)
    '''
    application = get_app()
    tornado.options.parse_command_line()
    application.listen(Options().port)
    iol = get_ioloop()
    iol.add_callback(log_is_ready)
    iol.start()

if __name__ == '__main__':
    main()
