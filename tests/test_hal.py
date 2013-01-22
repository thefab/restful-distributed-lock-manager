#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from rdlm.hal import Link, Resource

class HalTestCase(unittest.TestCase):

    def test_link(self):
        a = Link("/foo")
        b = Link("/foo", title="bar")
        tmp1 = a.to_dict()
        tmp2 = b.to_dict()
        self.assertEqual(tmp1['href'], "/foo")
        self.assertEqual(tmp2['href'] , "/foo")
        self.assertTrue("title" not in tmp1)
        self.assertTrue("title" in tmp2)
        self.assertEqual(tmp2['title'], "bar")

    def test_resource1(self):
        a = Resource("/foo")
        tmp = a.to_dict()
        self.assertEqual(tmp['_links']['self']['href'], '/foo')
        
    def test_resource2(self):
        a = Resource("/foo", {'key1': 'value1', 'key2': 'value2'})
        tmp = a.to_dict()
        self.assertEqual(tmp['key1'], 'value1')
        self.assertEqual(tmp['key2'], 'value2')
        
    def test_resource3(self):
        a = Resource("/foo", {'key1': 'value1', 'key2': 'value2'})
        b = Resource("/bar", {'key3': 'value3', 'key4': 'value4'})
        a.add_embedded_resource("bars", b)
        tmp = a.to_dict()
        self.assertEqual(tmp["_embedded"]['bars'][0]['key3'], 'value3')
        self.assertEqual(tmp["_embedded"]['bars'][0]['key4'], 'value4')
        
        