#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.abstract_lock_handler import AbstractLockHandler
from rdlm.lock import LOCK_MANAGER_INSTANCE

class LocksHandler(AbstractLockHandler):
    """Class which handles the /locks/[...]/ URL"""

    SUPPORTED_METHODS = ['GET', 'DELETE']

    def get(self, name, uid): # pylint: disable-msg=W0221
        '''
        @summary: deals with GET request
        @param name: name of the resource
        @param uid: uid of the lock
        '''    
        active_lock = LOCK_MANAGER_INSTANCE.get_active_lock(name)
        if active_lock and (active_lock.uid == uid):
            self.set_header('Content-Type', 'application/json')
            self.write(active_lock.to_json())
        else:
            self.send_error(status_code=404)
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
            self.set_status(204)
            self.finish()
        else:
            self.send_error(status_code=404)
            return
