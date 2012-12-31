#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

import tornado.web
import traceback
import httplib

class RequestHandler(tornado.web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        if self.settings.get("debug") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            if kwargs.has_key('message'):
                message = kwargs['message']
            else:
                message = httplib.responses[status_code]
            self.finish("<html><title>%(code)d: %(message)s</title>"
                        "<body>%(code)d: %(message)s</body></html>" % {
                        "code": status_code,
                        "message": message,
                        })
