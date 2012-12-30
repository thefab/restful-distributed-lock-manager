#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

from rdlm.request_handler import RequestHandler

class AbstractLockHandler(RequestHandler):
    """Just an abstract class to store some utilities methods"""

    def get_base_url(self, request):
        '''
        @summary: returns the http://hostname:port part of an url
        @param request: incoming HttpRequest object (from tornado)
        @result: the http://hostname:port part of an url

        The base url is built from another incoming http request
        to get the correct hostname and port as choosen by the 
        client (in order to avoid some problems with proxy 
        configurations)
        '''
        return "%s://%s" % (request.protocol, request.host)