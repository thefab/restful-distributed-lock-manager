#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

import uuid
import datetime
import collections
import json
import logging


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
        self.wait_expires = self.wait_since + datetime.timedelta(seconds=wait)

    def delete(self, timeout=True):
        '''
        @summary: explicit destructor
        @param timeout: if True, the delete is made by a timeout
        '''
        if self.__delete_callback:
            (self.__delete_callback)(timeout=timeout)
        self.reset_callbacks()

    @classmethod
    def from_json(cls, resource_name, json_string):
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

    def to_dict(self):
        '''
        @summary: method which dumps the lock object as a python dict
        @result: python dict
        '''
        tmp = {"uid": self.uid,
               "title": self.title,
               "wait": self.wait,
               "lifetime": self.lifetime,
               "active": self.__active}
        if self.__active:
            tmp['active_since'] = self.active_since.isoformat()
            tmp['active_expires'] = self.active_expires.isoformat()
        else:
            tmp['wait_since'] = self.wait_since.isoformat()
            tmp['wait_expires'] = self.wait_expires.isoformat()
        return tmp

    def to_json(self):
        '''
        @summary: method which dumps the lock object as a json string
        @result: json string
        '''
        tmp = self.to_dict()
        return json.dumps(tmp, indent=4, sort_keys=True)

    def set_active(self):
        '''
        @summary: change the status of the lock to active (corresponding callback is invoked)
        '''
        self.wait_since = None
        self.wait_expires = None
        self.__active = True
        self.active_since = datetime.datetime.now()
        self.active_expires = self.active_since + datetime.timedelta(seconds=self.lifetime)
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
        @summary: returns True is the lock is expired (wait timeout or lifetime timeout
                  depending on the status)
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
    __waiting_locks = None

    def __init__(self, name):
        '''
        @summary: constructor
        @param name: name of the resource
        '''
        self.name = name
        self.active_lock = None
        self.__waiting_locks = collections.deque()

    def to_dict(self):
        '''
        @summary: method which dumps the resource as a python dict
        @result: python dict
        '''
        tmp = {}
        tmp["name"] = self.name
        tmp["locks"] = []
        if self.active_lock:
            tmp["locks"].append(self.active_lock.to_dict())
        for waiting_lock in self.__waiting_locks:
            tmp["locks"].append(waiting_lock.to_dict())
        return tmp

    def to_json(self):
        '''
        @summary: method which dumps the resource object as a json string
        @result: json string
        '''
        tmp = self.to_dict()
        return json.dumps(tmp, indent=4, sort_keys=True)

    def delete(self, uid=None):
        '''
        @summary: delete all locks of the resource (uid=None) or a specific lock (uid!=None)
        @param uid: uid of the lock to delete (or None to delete all)
        @result: True if there was at least a lock, False else
        '''
        tmp_queue = collections.deque()
        res = False
        while True:
            try:
                lock = self.__waiting_locks.popleft()
                if not(uid):
                    lock.delete(timeout=False)
                    res = True
                else:
                    if lock.uid == uid:
                        lock.delete(timeout=False)
                        res = True
                    else:
                        tmp_queue.append(lock)
            except IndexError:
                break
        self.__waiting_locks = tmp_queue
        res = res or self.remove_active_lock(timeout=False, uid=uid)
        return res

    def get(self, uid):
        '''
        @summary: return the lock with the given uid
        @param uid: uid of the lock to get
        @result: lock object (or None)
        '''
        for lock in self.__waiting_locks:
            if lock.uid == uid and not(lock.is_expired()):
                return lock
        if self.active_lock and not(self.active_lock.is_expired()):
            if self.active_lock.uid == uid:
                return self.active_lock

    def remove_active_lock(self, timeout=True, uid=None):
        '''
        @summary: remove the active lock of the resource (if any)
        @param timeout: if True, the delete is made by a timeout
        @param uid: uid of the lock to delete (or None to delete
                    the active lock without specific test)
        @result: True if there was an active lock, False else

        Of course, if there is some non expired waiting locks,
        the first one is promoted as the active lock of the resource
        '''
        if self.active_lock:
            if not(uid) or self.active_lock.uid == uid:
                self.active_lock.delete(timeout=timeout)
                self.active_lock = None
                while True:
                    try:
                        lock = self.__waiting_locks.popleft()
                        if lock.is_expired():
                            lock.delete(timeout=timeout)
                            continue
                        lock.set_active()
                        self.active_lock = lock
                        break
                    except IndexError:
                        break
                return True
        return False

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
            self.__waiting_locks.append(lock)

    def clean_expired_locks(self):
        '''
        @summary: clean expired lock of the resource (active and waiting)
        '''
        tmp_queue = collections.deque()
        while True:
            try:
                lock = self.__waiting_locks.popleft()
                if lock.is_expired():
                    logging.warning("Expired waiting lock [%s] on [%s] => removing it" % (
                                    lock.title, self.name))
                    lock.delete()
                    continue
                tmp_queue.append(lock)
            except IndexError:
                break
        self.__waiting_locks = tmp_queue
        if self.active_lock and self.active_lock.is_expired():
            logging.warning("Expired active lock [%s] on [%s] => releasing it" % (
                            self.active_lock.title, self.name))
            self.remove_active_lock()


class LockManager(object):
    '''
    Class which managers resources

    Designed to be used as a singleton
    '''

    __resources_dict = None

    def __init__(self):
        '''
        @summary: constructor
        @result: ResourceManager object
        '''
        self.__resources_dict = {}

    def remove_all_resources(self):
        '''
        @summary: remove all resources
        '''
        resource_names = self.get_resources_names()
        for name in resource_names:
            self.remove_resource(name)
        self.__resources_dict = {}

    def get_resources_names(self):
        '''
        @summary: returns a python list with resource names
        @result: python list of strings
        '''
        return list(self.__resources_dict.keys())

    def get_resource_as_dict(self, resource_name):
        '''
        @summary: returns the given resource as a python dict
        @param resource_name: name of resource
        @result: python dict
        '''
        if resource_name not in self.__resources_dict:
            return None
        return self.__resources_dict[resource_name].to_dict()

    def remove_resource(self, resource_name):
        '''
        @summary: remove a resource (and its locks)
        @param resource_name: name of the resource
        @result: True if there was at least one lock, False else
        '''
        if resource_name in self.__resources_dict:
            res = self.__resources_dict[resource_name].delete()
            del(self.__resources_dict[resource_name])
            return res
        return False

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
        if resource_name not in self.__resources_dict:
            self.__resources_dict[resource_name] = Resource(resource_name)
        resource = self.__resources_dict[resource_name]
        resource.add_lock(lock)

    def delete_lock(self, resource_name, uid):
        '''
        @summary: delete a specific lock for the given resource
        @param resource_name: name of the resource
        @param uid: uid of the lock to delete
        @param lock: True if something has been deleted (False else)
        '''
        if resource_name not in self.__resources_dict:
            self.__resources_dict[resource_name] = Resource(resource_name)
        resource = self.__resources_dict[resource_name]
        return resource.delete(uid)

    def get_lock(self, resource_name, uid):
        '''
        @summary: get a specific lock for the given resource
        @param resource_name: name of the resource
        @param uid: uid of the lock to get
        @param lock: lock object (or None if not found)
        '''
        if resource_name not in self.__resources_dict:
            self.__resources_dict[resource_name] = Resource(resource_name)
        resource = self.__resources_dict[resource_name]
        return resource.get(uid)

    def clean_expired_locks(self):
        '''
        @summary: clean expired lock of all resources (active and waiting)
        '''
        names = self.get_resources_names()
        for name in names:
            self.__resources_dict[name].clean_expired_locks()


LOCK_MANAGER_INSTANCE = LockManager()
