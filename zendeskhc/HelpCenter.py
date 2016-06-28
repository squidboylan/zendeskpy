from __future__ import print_function
import requests
import json
import sys
from zendeskhc.ZendeskBase import Base

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

    # Article functions

    def list_all_articles(self):
        url = self.domain + '/api/v2/help_center/articles.json?per_page=100'
        return self._page_gets(url, 'articles')

    def list_articles_by_locale(self, locale):
        url = self.domain + '/api/v2/help_center/{locale}/articles.json?per_page=100'.format(locale=locale)
        return self._page_gets(url, 'articles')

    def list_articles_by_category(self, category_id):
        url = self.domain + '/api/v2/help_center/categories/{id}/articles.json?per_page=100'.format(id=category_id)
        return self._page_gets(url, 'articles')

    def list_articles_by_section(self, section_id):
        url = self.domain + '/api/v2/help_center/sections/{id}/articles.json?per_page=100'.format(id=section_id)
        return self._page_gets(url, 'articles')

    def list_articles_by_user(self, user_id):
        url = self.domain + '/api/v2/help_center/users/{id}/articles.json?per_page=100'.format(id=user_id)
        return self._page_gets(url, 'articles')

    def list_articles_by_change(self, start_time):
        url = self.domain + '/api/v2/help_center/incremental/articles.json?start_time={start_time}?per_page=100'.format(start_time=start_time)
        return self._page_gets(url, 'articles')

    def show_article(self, article_id, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/articles/{id}.json'.format(id=article_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/articles/{id}.json'.format(id=article_id, locale=locale)

        return self.get(url, self.email, self.password)

    def create_article(self, section_id, data, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/sections/{id}/articles.json'.format(id=section_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/sections/{id}/articles.json'.format(id=section_id, locale=locale)

        return self.post(url, data, self.email, self.password)

    def update_article_metadata(self, article_id, data, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/articles/{id}.json'.format(id=article_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/articles/{id}.json'.format(id=article_id, locale=locale)

        return self.put(url, data, self.email, self.password)

    # Translation functions

    def list_translations_by_article(self, article_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/translations.json'.format(article_id=article_id)
        return self._page_gets(url, 'translations')

    def list_translations_by_section(self, section_id):
        url = self.domain + '/api/v2/help_center/sections/{section_id}/translations.json'.format(section_id=section_id)
        return self._page_gets(url, 'translations')

    def list_translations_by_category(self, category_id):
        url = self.domain + '/api/v2/help_center/categories/{category_id}/translations.json'.format(category_id=category_id)
        return self._page_gets(url, 'translations')

    def list_missing_translations_by_article(self, article_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/translations/missing.json'.format(article_id=article_id)
        return self.get(url, self.email, self.password)

    def list_missing_translations_by_section(self, section_id):
        url = self.domain + '/api/v2/help_center/sections/{section_id}/translations/missing.json'.format(section_id=section_id)
        return self.get(url, self.email, self.password)

    def list_missing_translations_by_category(self, category_id):
        url = self.domain + '/api/v2/help_center/categories/{category_id}/translations/missing.json'.format(category_id=category_id)
        return self.get(url, self.email, self.password)

    def show_translation(self, article_id, locale):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/translations/{locale}.json'.format(article_id=article_id, locale=locale)
        return self.get(url, self.email, self.password)

    def create_article_translation(self, article_id, data):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/translations.json'.format(article_id=article_id)
        return self.post(url, data, self.email, self.password)

    def create_section_translation(self, section_id, data):
        url = self.domain + '/api/v2/help_center/section/{section_id}/translations.json'.format(section_id=section_id)
        return self.post(url, data, self.email, self.password)

    def create_category_translation(self, category_id, data):
        url = self.domain + '/api/v2/help_center/categories/{category_id}/translations.json'.format(category_id=category_id)
        return self.post(url, data, self.email, self.password)

    def update_article_translation(self, article_id, data, locale):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/translations/{locale}.json'.format(article_id=article_id)
        return self.put(url, data, self.email, self.password)

    def update_section_translation(self, section_id, data, locale):
        url = self.domain + '/api/v2/help_center/section/{section_id}/translations/{locale}.json'.format(section_id=section_id)
        return self.put(url, data, self.email, self.password)

    def update_category_translation(self, category_id, data, locale):
        url = self.domain + '/api/v2/help_center/categories/{category_id}/translations/{locale}.json'.format(category_id=category_id)
        return self.put(url, data, self.email, self.password)

    def delete_translation(self, translation_id):
        url = self.domain + '/api/v2/help_center/translations/{id}.json'.format(id=translation_id)
        return self.delete(url, self.email, self.password)

    def list_enabled_and_default_locales(self):
        url = self.domain + '/api/v2/help_center/locales.json'
        return self.get(url, self.email, self.password)

    # Section functions

    def list_all_sections(self):
        url = self.domain + '/api/v2/help_center/sections.json'
        return self._page_gets(url, 'sections')

    def list_sections_by_locale(self, locale):
        url = self.domain + '/api/v2/help_center/{locale}/sections.json'.format(locale=locale)
        return self._page_gets(url, 'sections')

    def list_sections_by_category(self, category_id):
        url = self.domain + '/api/v2/help_center/categories/{category_id}/sections.json'.format(category_id=category_id)
        return self._page_gets(url, 'sections')

    def show_section(self, section_id, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/sections/{id}.json'.format(id=section_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/sections/{id}.json'.format(locale=locale, id=section_id)

        return self.get(url, self.email, self.password)

    def create_section(self, category_id, data, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/categories/{id}.json'.format(id=section_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/categories/{id}.json'.format(locale=locale, id=section_id)

        return self.post(url, data, self.email, self.password)

    def update_section(self, section_id, data, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/sections/{id}.json'.format(id=section_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/sections/{id}.json'.format(locale=locale, id=section_id)

        return self.put(url, data, self.email, self.password)

    def update_section_source_locale(self, section_id, data):
        url = self.domain + '/api/v2/help_center/sections/{id}/source_locale.json'.format(id=section_id)
        return self.put(url, data, self.email, self.password)

    def delete_section(self, section_id):
        url = self.domain + '/api/v2/help_center/sections/{id}.json'.format(id=section_id)
        return self.delete(url, self.email, self.password)

    # Category functions

    def list_all_categories(self):
        url = self.domain + '/api/v2/help_center/categories.json'
        return self._page_gets(url, 'categories')

    def list_categories_by_locale(self, locale):
        url = self.domain + '/api/v2/help_center/{locale}/categories.json'.format(locale=locale)
        return self._page_gets(url, 'categories')

    def show_category(self, category_id, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/categories/{id}.json'.format(id=category_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/categories/{id}.json'.format(locale=locale, id=category_id)

        return self.get(url, self.email, self.password)

    def create_category(self, data, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/categories.json'
        else:
            url = self.domain + '/api/v2/help_center/{locale}/categories.json'.format(locale=locale)

        return self.post(url, data, self.email, self.password)

    def update_category(self, category_id, data, locale=None):
        if not locale:
            url = self.domain + '/api/v2/help_center/categories/{id}.json'.format(id=category_id)
        else:
            url = self.domain + '/api/v2/help_center/{locale}/categories/{id}.json'.format(locale=locale, id=category_id)

        return self.put(url, data, self.email, self.password)

    def update_category_source_locale(self, category_id, data):
        url = self.domain + '/api/v2/help_center/categories/{id}/source_locale.json'.format(id=category_id)
        return self.put(url, data, self.email, self.password)

    def delete_category(self, category_id):
        url = self.domain + '/api/v2/help_center/categories/{id}.json'.format(id=category_id)
        return self.delete(url, self.email, self.password)

    # Comment Functions

    def list_comments_by_user(self, user_id):
        url = self.domain + '/api/v2/help_center/users/{id}/comments.json'.format(id=user_id)
        return self._page_gets(url, 'comments')

    def list_comments_by_article(self, article_id):
        url = self.domain + '/api/v2/help_center/articles/{id}/comments.json'.format(id=article_id)
        return self._page_gets(url, 'comments')

    def show_comment(self, article_id, user_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/comments/{id}.json'.format(article_id=article_id, id=user_id)
        return self.get(url, self.email, self.password)

    def create_comment(self, article_id, data):
        url = self.domain + '/api/v2/help_center/articles/{id}/comments.json'.format(id=article_id)
        return self.post(url, data, self.email, self.password)

    def update_comment(self, article_id, comment_id, data):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/comments/{id}.json'.format(article_id=article_id, id=comment_id)
        return self.put(url, data, self.email, self.password)

    def delete_comment(self, article_id, comment_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/comments/{id}.json'.format(article_id=article_id, id=comment_id)
        return self.delete(url, self.email, self.password)

    # Labels Functions

    def list_all_labels(self):
        url = self.domain + '/api/v2/help_center/articles/labels.json'
        return self._page_gets(url, 'labels')

    def list_labels_by_article(self, article_id):
        url = self.domain + '/api/v2/help_center/articles/{id}/labels.json'.format(id=article_id)
        return self._page_gets(url, 'labels')

    def show_label(self, label_id):
        url = self.domain + '/api/v2/help_center/articles/labels/{id}.json'.format(id=label_id)
        return self.get(url, self.email, self.password)

    def create_label(self, article_id, data):
        url = self.domain + '/api/v2/help_center/articles/{id}/labels.json'.format(id=article_id)
        return self.post(url, data, self.email, self.password)

    def delete_label(self, article_id, label_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/labels/{id}.json'.format(article_id=article_id, id=label_id)
        return self.delete(url, self.email, self.password)

    # Article Search functions

    def search_articles_by_labels(self, labels):
        labels_string = ''
        for i in labels:
            labels_string = labels_string + i + ','
        url = self.domain + '/api/v2/help_center/articles.json?label_names=' + labels_string
        return self._page_gets(url, 'labels')

if __name__ == "__main__":
    domain = sys.argv[1]
    hc = HelpCenter(domain)
    derp = hc.get_all_articles()
    print(derp)
