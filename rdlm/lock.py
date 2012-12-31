#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

import uuid
import datetime
import collections
import json

class Lock(object):
    '''
    Class which defines a Lock object

    The lock object has a status :
    - active (the lock is acquired)
    - not active (the lock is not acquired)
    '''

    __active = False
    uid = None
    title = None
    resource_name = None
    lifetime = 0
    wait = 0
    wait_since = None
    wait_expires = None
    active_since = None
    active_expires = None
    __active_callback = None
    __delete_callback = None

    def __init__(self, resource_name, title, wait, lifetime):
        '''
        @summary: lock constructor
        @param resource_name: name of the resource to lock
        @param title: title of the lock
        @param wait: wait max duration (in seconds)
        @param lifetime: timeout of the lock (in seconds)
        @result: lock object (not active) 
        '''
        self.resource_name = resource_name
        self.lifetime = lifetime
        self.title = title
        self.uid = str(uuid.uuid4()).replace('-', '')
        self.wait = wait
        self.lifetime = lifetime
        self.wait_since = datetime.datetime.now()
        self.wait_expires = self.wait_since + datetime.timedelta(seconds = wait)

    def delete(self):
        '''
        @summary: explicit destructor
        '''
        if self.__delete_callback:
            (self.__delete_callback)()
        self.reset_callbacks()

    @classmethod
    def from_json(self, resource_name, json_string):
        '''
        @summary: class method which build a lock object from the corresponding json string
        @param resource_name: name of the resource
        @param json_string: json string
        @result: lock object (not active) or None if unseriliaze errors
        '''
        try:
            tmp = json.loads(json_string)
            title = tmp['title']
            wait = int(tmp['wait'])
            lifetime = int(tmp['lifetime'])
        except (KeyError, ValueError):
            return None
        return Lock(resource_name, title, wait, lifetime)

    def to_json(self):
        '''
        @summary: method which dumps the lock object as a json string
        @result: json string
        '''
        tmp = {"title": self.title,
               "wait": self.wait,
               "lifetime": self.lifetime}
        return json.dumps(tmp, indent=4, sort_keys=True)

    def set_active(self):
        '''
        @summary: change the status of the lock to active (corresponding callback is invoked)
        '''
        self.wait_since = None
        self.wait_expires = None
        self.__active = True
        self.active_since = datetime.datetime.now()
        self.active_expires = self.active_since + datetime.timedelta(seconds = self.lifetime)
        if self.__active_callback:
            (self.__active_callback)()
        self.reset_callbacks()
        
    def set_callbacks(self, active_callback, delete_callback):
        '''
        @summary: setter for callbacks
        @param active_callback: active callback
        @param delete_callback: delete callback
        '''
        self.__active_callback = active_callback
        self.__delete_callback = delete_callback

    def reset_callbacks(self):
        '''
        @summary: reset the lock callbacks
        '''
        self.__active_callback = None
        self.__delete_callback = None

    def is_expired(self):
        '''
        @summary: returns True is the lock is expired (wait timeout or lifetime timeout depending on the status)
        @result: True (the lock is expired) or False
        '''
        if self.__active:
            return (datetime.datetime.now() > self.active_expires)
        else:
            return (datetime.datetime.now() > self.wait_expires)


class Resource(object):
    """Class which defines a Resource object"""

    name = None
    active_lock = None
    __waiter_locks = None

    def __init__(self, name):
        '''
        @summary: constructor
        @param name: name of the resource
        '''
        self.name = name
        self.active_lock = None
        self.__waiter_locks = collections.deque()

    def remove_active_lock(self):
        '''
        @summary: remove the active lock of the resource (if any)
        
        Of course, if there is some non expired waiting locks,
        the first one is promoted as the active lock of the resource
        '''
        if self.active_lock:
            self.active_lock.delete()     
            self.active_lock = None
            while True:
                try:
                    lock = self.__waiter_locks.popleft()
                    if lock.is_expired():
                        lock.delete()
                        continue
                    lock.set_active()
                    self.active_lock = lock
                except IndexError:
                    break

    def add_lock(self, lock):
        '''
        @summary: add a lock to the resource
        @param lock: lock object
        
        If there is no active lock, the lock is promoted as the active
        lock for the resource

        If there is alreay an active lock, the lock is added to the 
        waiting list
        '''
        
        if not(self.active_lock):
            lock.set_active()
            self.active_lock = lock
        else:
            self.__waiter_locks.append(lock)

    def clean_expired_locks(self):
        '''
        @summary: clean expired lock of the resource (active and waiting)
        '''
        tmp_queue = collections.deque()
        while True:
            try:
                lock = self.__waiter_locks.popleft()
                if lock.is_expired():
                    lock.delete()
                    continue
                tmp_queue.append(lock)
            except IndexError:
                break
        self.__waiter_locks = tmp_queue
        if self.active_lock and self.active_lock.is_expired():
            self.remove_active_lock()


class LockManager(object):

    __resources_dict = {}

    def _reinit(self):
        '''
        @summary: reinitialize the lock manager (for unit testing only) 
        '''
        self.__resources_dict = {}

    def add_lock(self, resource_name, lock):
        '''
        @summary: add a lock to the resource
        @param resource_name: name of the resource
        @param lock: lock object
        
        If there is no active lock, the lock is promoted as the active
        lock for the resource

        If there is alreay an active lock, the lock is added to the 
        waiting list
        '''
        if not(self.__resources_dict.has_key(resource_name)):
            self.__resources_dict[resource_name] = Resource(resource_name)
        resource = self.__resources_dict[resource_name]
        resource.add_lock(lock)

    def remove_active_lock(self, resource_name):
        '''
        @summary: remove the active lock of the resource (if any)
        @param resource_name: name of the resource

        Of course, if there is some non expired waiting locks,
        the first one is promoted as the active lock of the resource
        '''
        if not(self.__resources_dict.has_key(resource_name)):
            self.__resources_dict[resource_name] = Resource(resource_name)
        resource = self.__resources_dict[resource_name]
        resource.remove_active_lock()

    def get_active_lock(self, resource_name):
        '''
        @summary: return the active lock for the resource name
        @param resource_name: name of the resource
        @result: active lock object (or None)
        '''
        if not(self.__resources_dict.has_key(resource_name)):
            self.__resources_dict[resource_name] = Resource(resource_name)
        resource = self.__resources_dict[resource_name]
        return resource.active_lock

    def clean_expired_locks(self):
        '''
        @summary: clean expired lock of all resources (active and waiting)
        '''
        names = self.__resources_dict.keys()
        for name in names:
            self.__resources_dict[name].clean_expired_locks()


LOCK_MANAGER_INSTANCE = LockManager()