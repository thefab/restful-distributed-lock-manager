#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler, admin_authenticated
from rdlm.lock import LOCK_MANAGER_INSTANCE

class ResourceHandler(RequestHandler):
    """Class which handles the /resources/[resource] URL"""

    SUPPORTED_METHODS = ['GET', 'DELETE']

    @admin_authenticated
    def delete(self, name): # pylint: disable-msg=W0221
        res = LOCK_MANAGER_INSTANCE.remove_resource(name)
        if res:
            self.set_status(204)
            self.finish()
        else:
            self.send_error(404, message="no resource (with locks) found")