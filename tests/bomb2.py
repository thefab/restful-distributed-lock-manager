#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing import Pool
import requests

PROCESS_POOL_SIZE = 10
REQUESTS = 10000
BASE_URL = "http://localhost:8888"
RESOURCE_NAME_PREFIX = "resource"

def f(process_number):
    resource_name = "%s%i" % (RESOURCE_NAME_PREFIX, process_number)
    raw_body = '{"title": "%i", "lifetime": 300, "wait": 20}' % process_number
    r = requests.post("%s/active_locks/%s" % (BASE_URL, resource_name), data=raw_body)
    if r.status_code != 201:
        raise Exception("bad status code %i from post request" % r.status_code)
    lock_url = r.headers['Location']
    r = requests.delete(lock_url)
    if r.status_code != 204:
        raise Exception("bad status code %i from delete request" % r.status_code)
 
if __name__ == '__main__':
    pool = Pool(processes=PROCESS_POOL_SIZE)
    pool.map(f, range(0, REQUESTS))
