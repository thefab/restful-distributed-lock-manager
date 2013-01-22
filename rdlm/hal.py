#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of restful-distributed-lock-manager released under the MIT license.
# See the LICENSE file for more information.

import json
import collections
import copy

class Link(object):
    '''
    Class which defines a HAL Link object
    '''

    href = None
    title = None

    def __init__(self, href, title = None):
        '''
        @summary: constructor
        @param href: href target
        @param title: title of the link
        @result: HAL Link object
        '''
        self.href = href
        self.title = title

    def to_dict(self):
        '''
        @summary: returns the HAL Link object as a python dict
        @result: python dict
        '''
        if self.title:
            return { "href": self.href, "title": self.title }
        else:
            return { "href": self.href }

class Resource(object):
    '''
    Class which defines a HAL Resource object
    '''   

    properties = None
    links = None
    embedded_resources = None

    def __init__(self, href, properties = None):
        '''
        @summary: constructor
        @param href: href target
        @param properties: python dict of properties as key => value
        @result: HAL Resource object
        '''
        if properties:
            self.properties = copy.copy(properties)
        else:
            self.properties = {}
        self.links = {}
        self.embedded_resources = {}
        self.add_link("self", Link(href))

    def add_property(self, name, value):
        '''
        @summary: adds a property to the resource
        @param name: name 
        @param value: value
        '''
        self.properties[name] = value

    def add_link(self, rel, link, multiple = False):
        '''
        @summary: adds a link to the resource
        @param rel: rel type
        @param link: HAL Link object to add
        @param multiple: if True, allow multiple links for the rel type
        '''
        if rel not in self.links and multiple:
            self.links[rel] = []
        if multiple:
            self.links[rel].append(link)
        else:
            self.links[rel] = link

    def add_embedded_resource(self, collection_name, resource):
        '''
        @summary: adds an embedded resource to the resource
        @param collection_name: name of the collection
        @param resource: HAL Resource object to add as embedded resource
        '''
        if collection_name not in self.embedded_resources:
            self.embedded_resources[collection_name] = []
        self.embedded_resources[collection_name].append(resource)

    def to_dict(self):
        '''
        @summary: returns the HAL Resource object as a python dict
        @result: python dict

        Note: the serialization is recursive (on embedded resources and on links)
        '''
        tmp = {}
        for name in self.properties:
            tmp[name] = self.properties[name]
        tmp["_links"] = {}
        for rel in self.links:
            if isinstance(self.links[rel], collections.Iterable):
                tmp["_links"][rel] = [x.to_dict() for x in self.links[rel]]
            else:
                tmp["_links"][rel] = self.links[rel].to_dict()
        if len(self.embedded_resources) > 0:
            tmp["_embedded"] = {}
        for collection_name in self.embedded_resources:
            tmp["_embedded"][collection_name] = [x.to_dict() for x in (self.embedded_resources[collection_name])]
        return tmp

    def to_json(self):
        '''
        @summary: returns the HAL Resource object as JSON
        @result: JSON serialization of the HAL Resource object
        '''
        return json.dumps(self.to_dict(), indent=4)
            


