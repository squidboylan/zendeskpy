from __future__ import print_function
import requests
import json
import sys
import time

class ZendeskError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Base:
    def get(self, url, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        response_raw = session.get(url)

        if response_raw.status_code == 429:
            time.sleep(response_raw.headers['Retry-After'])
            return get(url, email, password)

        else:
            if response_raw.headers['Content-Type'] == "application/json; charset=utf-8":
                response_json = json.loads(response_raw.content)
                return response_json
            else:
                return None

    def put(self, url, data, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        session.headers = {'Content-Type': 'application/json'}
        response_raw = session.put(url, data)

        if response_raw.status_code == 429:
            time.sleep(response_raw.headers['Retry-After'])
            return put(url, data, email, password)

        else:
            if response_raw.headers['Content-Type'] == "application/json; charset=utf-8":
                response_json = json.loads(response_raw.content)
                return response_json
            else:
                return None

    def post(self, url, data, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        session.headers = {'Content-Type': 'application/json'}
        response_raw = session.post(url, data)

        if response_raw.status_code == 429:
            time.sleep(response_raw.headers['Retry-After'])
            return put(url, data, email, password)

        else:
            if response_raw.headers['Content-Type'] == "application/json; charset=utf-8":
                response_json = json.loads(response_raw.content)
                return response_json
            else:
                return None

    def delete(self, url, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        response_raw = session.delete(url)

        if response_raw.status_code == 429:
            time.sleep(response_raw.headers['Retry-After'])
            return put(url, data, email, password)

        else:
            if response_raw.headers['Content-Type'] == "application/json; charset=utf-8":
                response_json = json.loads(response_raw.content)
                return response_json
            else:
                return None
