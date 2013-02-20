#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler, admin_authenticated
from rdlm.lock import LOCK_MANAGER_INSTANCE
from rdlm.hal import Resource

class ResourceHandler(RequestHandler):
    """Class which handles the /resources/[resource] URL"""

    SUPPORTED_METHODS = ['GET', 'DELETE']

    @admin_authenticated
    def delete(self, name): # pylint: disable-msg=W0221
        '''
        @summary: deals with DELETE request (deleting the given resource)
        @param name: name of the resource
        '''
        res = LOCK_MANAGER_INSTANCE.remove_resource(name)
        if res:
            self.send_status(204)
        else:
            self.send_error(404, message="no resource (with locks) found")

    @admin_authenticated
    def get(self, name): # pylint: disable-msg=W0221
        '''
        @summary: deals with GET request (getting a JSON HAL of the resource)
        @param name: name of the resource
        '''
        tmp = LOCK_MANAGER_INSTANCE.get_resource_as_dict(name)
        resource = Resource(self.reverse_url("resource", name), {"name": name})
        if not(tmp):
            for lock_dict in tmp['locks']:
                lock = Resource(self.reverse_url("lock", name, lock_dict['uid']), lock_dict)
                resource.add_embedded_resource("locks", lock)
        self.set_header("Content-Type", "application/hal+json")
        self.finish(resource.to_json())
