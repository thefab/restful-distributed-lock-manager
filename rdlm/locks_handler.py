#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler
from rdlm.lock import Lock
import tornado.web
import tornado.gen
import tornado.ioloop
from rdlm.lock import LOCK_MANAGER_INSTANCE
import functools


class LocksHandler(RequestHandler):
    """Class which handles the /locks/[resource] URL"""

    def on_active_wrapper(self, name, lock):
        '''
        @summary: wrapper method to invoke on_active method through tornado ioloop
        @param name: name of the resource
        @param lock: lock object
        '''
        tornado.ioloop.IOLoop.instance().add_callback(functools.partial(self.on_active,
                                                                        name, lock))

    def on_delete_wrapper(self, admin=False):
        '''
        @summary: wrapper method to invoke on_delete method through tornado ioloop
        @param admin: if True, the delete is made by an admin request
        '''
        tornado.ioloop.IOLoop.instance().add_callback(functools.partial(self.on_delete,
                                                                        admin=admin))

    def on_active(self, name, lock):
        '''
        @summary: method called when the lock becomes active
        @param name: name of the resource
        @param lock: lock object

        The method returns an HTTP/201 in this case with
        the corresponding Location header
        '''
        url = "%s%s" % (self.get_base_url(self.request), self.reverse_url("lock", name, lock.uid))
        self.send_status(201, message="lock acquired at %s" % url, headers={"Location": url})

    def on_delete(self, admin=False):
        '''
        @summary: method called when the wait for the lock is over
        @param admin: True if the delete is made by an admin request

        The method returns an HTTP/408 or an HTTP/409 in this case
        (depending if the delete is made by an admin request)
        '''
        if admin:
            self.send_error(status_code=409, message="lock request deleted by an admin request")
        else:
            self.send_error(status_code=408, message="lock request (wait) timeout")

    @tornado.web.asynchronous
    def post(self, name):
        '''
        @summary: deals with POST request (acquiring locks on resource)
        @param name: name of the resource
        '''
        raw_body = self.request.body.decode('utf-8')
        if len(raw_body) == 0:
            self.send_error(status_code=400, message="empty body")
            return
        lock = Lock.from_json(name, raw_body)
        if not(lock):
            self.send_error(status_code=400, message="invalid json body")
            return
        lock.set_callbacks(functools.partial(self.on_active_wrapper, name, lock),
                           self.on_delete_wrapper)
        LOCK_MANAGER_INSTANCE.add_lock(name, lock)
