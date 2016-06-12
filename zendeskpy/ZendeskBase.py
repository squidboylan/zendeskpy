from __future__ import print_function
import requests
import json
import sys
import time

class Base:
    def get(self, url, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        response_raw = session.get(url)

        if response_raw.status_code == 429:
            time.sleep(response_raw.headers['Retry-After'])
            return get(url, email, password)

        else:
            response_json = json.loads(response_raw.content)
            return response_json

    def put(self, url, data, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        session.headers = {'Content-Type': 'application/json'}
        response_raw = session.put(url, data)

        if response_raw.status_code == 429:
            time.sleep(response_raw.headers['Retry-After'])
            return put(url, data, email, password)

        else:
            return response_raw

    def post(self, url, data, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        session.headers = {'Content-Type': 'application/json'}
        response_raw = session.post(url, data)

        if response_raw.status_code == 429:
            time.sleep(response_raw.headers['Retry-After'])
            return put(url, data, email, password)

        else:
            return response_raw