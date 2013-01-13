#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler, admin_authenticated
from rdlm.lock import LOCK_MANAGER_INSTANCE

class ResourcesHandler(RequestHandler):
    """Class which handles the /resources URL"""

    SUPPORTED_METHODS = ['GET', 'DELETE']

    @admin_authenticated
    def delete(self): # pylint: disable-msg=W0221
        LOCK_MANAGER_INSTANCE.remove_all_resources()
        self.send_status(204)
