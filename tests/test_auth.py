#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.testing
from rdlm.main import get_app as rdlm_get_app
import os
import base64


class AuthTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return rdlm_get_app()

    def tearDown(self):
        self.set_config_file(["admin_userpass_file='yes'"])
        req = tornado.httpclient.HTTPRequest(self.get_url("/resources"), method='DELETE')
        self.http_client.fetch(req, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 204)
        super(AuthTestCase, self).tearDown()

    # compatibility with python 2.6
    def assertIn(self, str1, str2):
        self.assertTrue(str1 in str2)

    def current_dir(self):
        return os.path.dirname(__file__)

    def set_config_file(self, keyvalues):
        config_file = "%s/conf.py" % self.current_dir()
        with open(config_file, "w") as f:
            f.write("\n".join(keyvalues) + "\n")
        tornado.options.parse_config_file(config_file)

    def set_userpass_file(self, keyvalues):
        auth_file = "%s/auth.txt" % self.current_dir()
        with open(auth_file, "w") as f:
            f.write("\n".join(keyvalues) + "\n")
        self.set_config_file(["admin_userpass_file='%s'" % auth_file])

    def test_no(self):
        self.set_config_file(["admin_userpass_file='no'"])
        req = tornado.httpclient.HTTPRequest(self.get_url("/resources"), method='DELETE')
        self.http_client.fetch(req, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 403)

    def test_yes(self):
        self.set_config_file(["admin_userpass_file='yes'"])
        req = tornado.httpclient.HTTPRequest(self.get_url("/resources"), method='DELETE')
        self.http_client.fetch(req, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 204)

    def test_userpass(self):
        self.set_userpass_file(["foo:bar", "foo2:bar2", "foo3:bar3"])
        req = tornado.httpclient.HTTPRequest(self.get_url("/resources"), method='DELETE')
        self.http_client.fetch(req, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 401)
        b64 = base64.standard_b64encode("foo2:bar2")
        req = tornado.httpclient.HTTPRequest(self.get_url("/resources"),
                                             method='DELETE',
                                             headers={'Authorization': "Basic %s" % b64})
        self.http_client.fetch(req, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 204)
        b64 = base64.standard_b64encode("foo:bar2")
        req = tornado.httpclient.HTTPRequest(self.get_url("/resources"),
                                             method='DELETE',
                                             headers={'Authorization': "Basic %s" % b64})
        self.http_client.fetch(req, self.stop)
        response = self.wait()
        self.assertEqual(response.code, 401)
