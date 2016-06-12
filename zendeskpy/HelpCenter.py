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

    def _page_gets(self, url, combine_key):
        data = self.get(url, self.email, self.password)
        next_page_url = data['next_page']

        while next_page_url is not None:
            next_page_json = self.get(next_page_url, self.email, self.password)
            data[combine_key] = data[combine_key] + next_page_json[combine_key]
            next_page_url = next_page_json['next_page']

        data['next_page'] = None
        return data

    def get_all_articles(self):
        url = domain + '/api/v2/help_center/articles.json?per_page=100'
        return self._page_gets(url, 'articles')

    def get_articles_by_locale(self, locale):
        url = domain + '/api/v2/help_center/{locale}/articles.json?per_page=100'.format(locale=locale)
        return self._page_gets(url, 'articles')

    def get_articles_by_category(self, category_id):
        url = domain + '/api/v2/help_center/categories/{id}/articles.json?per_page=100'.format(id=category_id)
        return self._page_gets(url, 'articles')

    def get_articles_by_section(self, section_id):
        url = domain + '/api/v2/help_center/sections/{id}/articles.json?per_page=100'.format(id=section_id)
        return self._page_gets(url, 'articles')

    def get_articles_by_user(self, user_id):
        url = domain + '/api/v2/help_center/users/{id}/articles.json?per_page=100'.format(id=user_id)
        return self._page_gets(url, 'articles')

    def get_articles_by_change(self, start_time):
        url = domain + '/api/v2/help_center/incremental/articles.json?start_time={start_time}?per_page=100'.format(start_time=start_time)
        return self._page_gets(url, 'articles')

if __name__ == "__main__":
    domain = sys.argv[1]
    hc = HelpCenter(domain)
    derp = hc.get_all_articles()
    print(derp)
