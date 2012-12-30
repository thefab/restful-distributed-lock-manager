#!/usr/bin/python
# -*- coding: utf-8 -*-

import tornado.testing
from rdlm.main import get_app as rdlm_get_app

class HelloTestCase(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return rdlm_get_app()

    def test_home(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        self.assertIn("Welcome", response.body)
        self.assertEqual(response.code, 200)
        
