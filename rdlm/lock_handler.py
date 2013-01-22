#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler
from rdlm.lock import LOCK_MANAGER_INSTANCE
from rdlm.hal import Resource, Link

class LockHandler(RequestHandler):
    """Class which handles the /locks/[resource]/[uid] URL"""

    SUPPORTED_METHODS = ['GET', 'DELETE']

    def get(self, name, uid): # pylint: disable-msg=W0221
        '''
        @summary: deals with GET request
        @param name: name of the resource
        @param uid: uid of the lock
        '''    
        active_lock = LOCK_MANAGER_INSTANCE.get_active_lock(name)
        if active_lock and (active_lock.uid == uid):

            self.set_header('Content-Type', 'application/hal+json')
            hal_lock = Resource(href=self.reverse_url("lock", name, active_lock.uid), properties=active_lock.to_dict())
            hal_resource_link = Link(href=self.reverse_url("resource", name))
            hal_lock.add_link(rel="resource", link=hal_resource_link, multiple=False)
            self.write(hal_lock.to_json())
        else:
            self.send_error(status_code=404, message="lock not found")
            return

    def delete(self, name, uid): # pylint: disable-msg=W0221
        '''
        @summary: deals with DELETE request (releasing a lock)
        @param name: name of the resource
        @param uid: uid of the lock
        '''
        active_lock = LOCK_MANAGER_INSTANCE.get_active_lock(name)
        if active_lock and (active_lock.uid == uid):
            LOCK_MANAGER_INSTANCE.remove_active_lock(name)
            self.send_status(204)
        else:
            self.send_error(status_code=404, message="lock not found")
            return
