#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler, admin_authenticated
from rdlm.lock import LOCK_MANAGER_INSTANCE
from rdlm.hal import Resource

class ResourcesHandler(RequestHandler):
    """Class which handles the /resources URL"""

    SUPPORTED_METHODS = ['GET', 'DELETE']

    @admin_authenticated
    def delete(self): # pylint: disable-msg=W0221
        '''
        @summary: deals with DELETE request (deleting all resources)
        '''
        LOCK_MANAGER_INSTANCE.remove_all_resources()
        self.send_status(204)

    @admin_authenticated
    def get(self): # pylint: disable-msg=W0221
        '''
        @summary: deals with GET request (getting a JSON HAL of resources)
        '''
        resources = Resource(self.reverse_url("resources"))
        resources_names = LOCK_MANAGER_INSTANCE.get_resources_names()
        for resource_name in resources_names:
            tmp = LOCK_MANAGER_INSTANCE.get_resource_as_dict(resource_name)
            resource = Resource(self.reverse_url("resource", tmp['name']), {"name": tmp['name']})
            resources.add_embedded_resource("resources", resource)
        self.set_header("Content-Type", "application/hal+json")
        self.finish(resources.to_json())


    
