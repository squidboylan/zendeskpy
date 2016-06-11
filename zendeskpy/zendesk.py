from __future__ import print_function
import requests
import json
import sys

class Base:
    def get(self, url, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        response_raw = session.get(url)
        response_json = json.loads(response_raw.content)
        return response_json

    def put(self, url, data, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        session.headers = {'Content-Type': 'application/json'}
        r = session.put(url, data)
        return r

    def post(self, url, data, email=None, password=None):
        session = requests.Session()
        session.auth = (email, password)
        session.headers = {'Content-Type': 'application/json'}
        r = session.post(url, data)
        return r

class HelpCenter(Base):
    def __init__(self, domain, email=None, password=None):
        self.domain = domain
        self.email = email
        self.password = password

    def get_all_articles(self):
        return self.get(domain + '/api/v2/help_center/articles.json')

if __name__ == "__main__":
    domain = sys.argv[1]
    hc = HelpCenter(domain)
    derp = hc.get_all_articles()
    print(derp)
