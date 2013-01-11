#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

import tornado.web
import traceback
try:
    from httplib import responses
except ImportError:
    # Compatibility with Python3
    from http.client import responses # pylint: disable-msg=F0401
from rdlm.options import Options
import base64

def admin_authenticated(func):
    def wrapper(handler, *args, **kwargs): # pylint: disable-msg=W0613
        admin_userpass_file = Options().admin_userpass_file
        if admin_userpass_file == "yes":
            return func(handler, *args, **kwargs)
        if admin_userpass_file == "no":
            handler.send_error(403)
            return False
        auth_header = handler.request.headers.get('Authorization')
        if auth_header is not None and auth_header.startswith('Basic '):         
            auth_decoded = base64.decodestring(auth_header[6:])
            basicauth_user, basicauth_pass = auth_decoded.split(':', 2)
            try:
                with open(admin_userpass_file, "r") as f:
                    lines = f.readlines()
                    for line in lines:
                        username, password = line.strip().split(":", 1)
                        if (basicauth_user == username) and (basicauth_pass == password):
                            return func(handler, *args, **kwargs)
            except: # pylint: disable-msg=W0702
                handler.send_error(500, message="bad admin userpass file")
                return False
        handler.set_status(401)
        handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
        handler.finish()
        return False
    return wrapper

class RequestHandler(tornado.web.RequestHandler):
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

    def write_error(self, status_code, **kwargs):
        if self.settings.get("debug") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            if 'message' in kwargs:
                message = kwargs['message']
            else:
                message = responses[status_code]
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                        "code": status_code,
                        "message": message,
                        })
