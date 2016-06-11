from __future__ import print_function
import requests
import json
import sys
from ZendeskBase import Base

class HelpCenter(Base):
    def __init__(self, domain, email=None, password=None):
        self.domain = domain
        self.email = email
        self.password = password

    def get_all_articles(self):
        url = domain + '/api/v2/help_center/articles.json'
        return self.get(url)

    def get_articles_by_locale(self, locale):
        url = domain + '/api/v2/help_center/{locale}/articles.json'.format(locale=locale)
        return self.get(url)

    def get_articles_by_category(self, category_id):
        url = domain + '/api/v2/help_center/categories/{id}/articles.json'.format(id=category_id)
        return self.get(url)

    def get_articles_by_section(self, section_id):
        url = domain + '/api/v2/help_center/sections/{id}/articles.json'.format(id=section_id)
        return self.get(url)

    def get_articles_by_user(self, user_id):
        url = domain + '/api/v2/help_center/users/{id}/articles.json'.format(id=user_id)
        return self.get(url)

    def get_articles_by_change(self, start_time)
        url = domain + '/api/v2/help_center/incremental/articles.json?start_time={start_time}'.format(start_time=start_time)
        return self.get(url)

if __name__ == "__main__":
    domain = sys.argv[1]
    hc = HelpCenter(domain)
    derp = hc.get_all_articles()
    print(derp)
