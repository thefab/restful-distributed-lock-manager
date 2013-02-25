#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler


class HelloHandler(RequestHandler):
    """Class which handles the / URL"""

    def get(self):
        '''
        @summary: deals with GET request on /
        '''
        self.write('Welcome on restful-distributed-lock-manager !')
