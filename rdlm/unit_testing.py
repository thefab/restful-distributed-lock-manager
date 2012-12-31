#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler
from rdlm.lock import LOCK_MANAGER_INSTANCE

class UnitTestingHandler(RequestHandler):
    """Class which handles some unit testing handler URL"""

    def get(self):
        '''
        @summary: deals with GET request on /reset
        '''
        LOCK_MANAGER_INSTANCE._reinit() # pylint: disable-msg=W0212