from __future__ import print_function
import requests
import json
import sys
from zendeskhc.ZendeskBase import *

class HelpCenter(Base):
    def __init__(self, domain, email=None, password=None):
        self.domain = domain
        self.email = email
        self.password = password

    def _page_gets(self, url, combine_key):
        data = self.get(url, self.email, self.password)

        if 'error' in data.keys():
            raise ZendeskError(data['error'])

        next_page_url = data['next_page']

        while next_page_url is not None:
            next_page_json = self.get(next_page_url, self.email, self.password)
            data[combine_key] = data[combine_key] + next_page_json[combine_key]
            next_page_url = next_page_json['next_page']

        data['next_page'] = None
        return data

    def _generate_options(self, options=None):
        option_string = '?'

        if not options:
            options = {}

        if 'per_page' not in options.keys():
            options['per_page'] = 100

        for i in options.keys():
            option_string = option_string + i
            option_string = option_string + '='
            option_string = option_string + str(options[i])
            option_string = option_string + '&'

        return option_string

    # Article functions

    def list_all_articles(self, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles.json' + option_string
        return self._page_gets(url, 'articles')

    def list_articles_by_locale(self, locale, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/{locale}/articles.json' + option_string
        url = url.format(locale=locale)
        return self._page_gets(url, 'articles')

    def list_articles_by_category(self, category_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/categories/{id}/articles.json' + option_string
        url = url.format(id=category_id)
        return self._page_gets(url, 'articles')

    def list_articles_by_section(self, section_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/sections/{id}/articles.json' + option_string
        url = url.format(id=section_id)
        return self._page_gets(url, 'articles')

    def list_articles_by_user(self, user_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/users/{id}/articles.json' + option_string
        url = url.format(id=user_id)
        return self._page_gets(url, 'articles')

    def list_changed_articles(self, start_time, options=None):
        # start_time should be a Unix epoch time
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/incremental/articles.json?start_time={start_time}' + option_string
        url = url.format(start_time=start_time)
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

    def list_article_translations(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/translations.json' + option_string
        url = url.format(article_id=article_id)
        return self._page_gets(url, 'translations')

    def list_section_translations(self, section_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/sections/{section_id}/translations.json' + option_string
        url = url.format(section_id=section_id)
        return self._page_gets(url, 'translations')

    def list_category_translations(self, category_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/categories/{category_id}/translations.json' + option_string
        url = url.format(category_id=category_id)
        return self._page_gets(url, 'translations')

    def list_missing_article_translations(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/translations/missing.json' + option_string
        url = url.format(article_id=article_id)
        return self.get(url, self.email, self.password)

    def list_missing_section_translations(self, section_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/sections/{section_id}/translations/missing.json' + option_string
        url = url.format(section_id=section_id)
        return self.get(url, self.email, self.password)

    def list_missing_category_translations(self, category_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/categories/{category_id}/translations/missing.json' + option_string
        url = url.format(category_id=category_id)
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

    def list_all_sections(self, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/sections.json' + option_string
        return self._page_gets(url, 'sections')

    def list_sections_by_locale(self, locale, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/{locale}/sections.json' + option_string
        url = url.format(locale=locale)
        return self._page_gets(url, 'sections')

    def list_sections_by_category(self, category_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/categories/{category_id}/sections.json' + option_string
        url = url.format(category_id=category_id)
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

    def list_all_categories(self, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/categories.json' + option_string
        return self._page_gets(url, 'categories')

    def list_categories_by_locale(self, locale, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/{locale}/categories.json' + option_string
        url = url.format(locale=locale)
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

    def list_comments_by_user(self, user_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/users/{id}/comments.json' + option_string
        url = url.format(id=user_id)
        return self._page_gets(url, 'comments')

    def list_comments_by_article(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{id}/comments.json' + option_string
        url = url.format(id=article_id)
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

    def list_all_labels(self, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/labels.json' + option_string
        return self._page_gets(url, 'labels')

    def list_labels_by_article(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{id}/labels.json' + option_string
        url = url.format(id=article_id)
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

    # Article Attachments

    def list_article_attachments(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/attachments.json' + option_string
        url = url.format(article_id=article_id)
        return self._page_gets(url, 'article_attachments')

    def list_article_inline_attachments(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/attachments/inline.json' + option_string
        url = url.format(article_id=article_id)
        return self._page_gets(url, 'article_attachments')

    def list_article_block_attachments(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/attachments/block.json' + option_string
        url = url.format(article_id=article_id)
        return self._page_gets(url, 'article_attachments')

    def show_article_attachment(self, attachment_id):
        url = self.domain + '/api/v2/help_center/articles/attachments/{id}.json'.format(id=attachment_id)
        return self.get(url, self.email, self.password)

    def create_article_attachment(self, article_id, data):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/attachments.json'.format(article_id=article_id)
        return self.post(url, data, self.email, self.password)

    def create_unassociated_attachment(self, data):
        url = self.domain + '/api/v2/help_center/articles/attachments.json'
        return self.post(url, data, self.email, self.password)

    def delete_article_attachment(self, attachment_id, data):
        url = self.domain + '/api/v2/help_center/articles/attachments/{id}.json'.format(id=attachment_id)
        return self.delete(url, self.email, self.password)

    # Topic functions

    def list_all_topics(self, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/community/topics.json' + option_string
        return self._page_gets(url, 'topics')

    def show_topic(self, topic_id):
        url = self.domain + '/api/v2/community/topics/{id}.json'.format(id=topic_id)
        return self.get(url, self.email, self.password)

    def create_topic(self, data):
        url = self.domain + '/api/v2/community/topics.json'
        return self.post(url, data, self.email, self.password)

    def update_topic(self, topic_id, data):
        url = self.domain + '/api/v2/community/topics/{id}.json'.format(id=topic_id)
        return self.put(url, data, self.email, self.password)

    def delete_topic(self, topic_id):
        url = self.domain + '/api/v2/community/topics/{id}.json'.format(id=topic_id)
        return self.delete(url, self.email, self.password)

    # Post functions

    def list_all_posts(self, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/community/posts.json' + option_string
        return self._page_gets(url, 'posts')

    def list_posts_by_topic(self, topic_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/community/topics/{id}/posts.json' + option_string
        url = url.format(id=topic_id) 
        return self._page_gets(url, 'posts')

    def list_posts_by_user(self, user_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/community/users/{id}/posts.json' + option_string
        url = url.format(id=user_id)
        return self._page_gets(url, 'posts')

    def show_post(self, post_id):
        url = self.domain + '/api/v2/community/posts/{id}.json'.format(id=post_id)
        return self.get(url, self.email, self.password)

    def create_post(self, data):
        url = self.domain + '/api/v2/community/posts.json'
        return self.post(url, data, self.email, self.password)

    def update_post(self, post_id, data):
        url = self.domain = '/api/v2/community/posts/{id}.json'.format(id=post_id)
        return self.put(url, data, self.email, self.password)

    def delete_post(self, post_id):
        url = self.domain = '/api/v2/community/posts/{id}.json'.format(id=post_id)
        return self.delete(url, self.email, self.password)

    # Post comment functions

    def list_post_comments(self, post_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/community/posts/{post_id}/comments.json' + option_string
        url = url.format(post_id=post_id)
        return self._page_gets(url, 'comments')

    def list_post_comments_by_user(self, user_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/community/users/{id}/comments.json' + option_string
        url = url.format(id=user_id)
        return self._page_gets(url, 'comments')

    def show_post_comment(self, post_id, comment_id):
        url = self.domain + '/api/v2/community/posts/{post_id}/comments/{id}.json'.format(post_id=post_id, id=comment_id)
        return self.get(url, self.email, self.password)

    def create_post_comment(self, post_id, data):
        url = self.domain + '/api/v2/community/posts/{post_id}/comments.json'.format(post_id=post_id)
        return self.post(url, data, self.email, self.password)

    def update_post_comment(self, post_id, comment_id, data):
        url = self.domain + '/api/v2/community/posts/{post_id}/comments/{id}.json'.format(post_id=post_id, id=comment_id)
        return self.put(url, data, self.email, self.password)

    def delete_post_comment(self, post_id, comment_id):
        url = self.domain + '/api/v2/community/posts/{post_id}/comments/{id}.json'.format(post_id=post_id, id=comment_id)
        return self.delete(url, self.email, self.password)

    # Article Subscription functions

    def list_article_subscriptions(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/subscriptions.json' + option_string
        url = url.format(article_id=article_id)
        return self._page_gets(url, 'subscriptions')

    def show_article_subscription(self, article_id, subscription_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/subscriptions/{id}.json'.format(article_id=article_id, id=subscription_id)
        return self.get(url, self.email, self.password)

    def create_article_subscription(self, article_id, data):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/subscriptions.json'.format(article_id=article_id)
        return self.post(url, data, self.email, self.password)

    def delete_article_subscription(self, article_id, subscription_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/subscriptions/{id}.json'.format(article_id=article_id, id=subscription_id)
        return self.delete(url, self.email, self.password)

    # Section Subscription functions

    def list_section_subscriptions(self, section_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/sections/{section_id}/subscriptions.json' + option_string
        url = url.format(section_id=section_id)
        return self._page_gets(url, 'subscriptions')

    def show_section_subscription(self, section_id, subscription_id):
        url = self.domain + '/api/v2/help_center/sections/{section_id}/subscriptions/{id}.json'.format(section_id=section_id, id=subscription_id)
        return self.get(url, self.email, self.password)

    def create_section_subscription(self, section_id, data):
        url = self.domain + '/api/v2/help_center/sections/{section_id}/subscriptions.json'.format(section_id=section_id)
        return self.post(url, data, self.email, self.password)

    def delete_section_subscription(self, section_id, subscription_id):
        url = self.domain + '/api/v2/help_center/sections/{section_id}/subscriptions/{id}.json'.format(section_id=section_id, id=subscription_id)
        return self.delete(url, self.email, self.password)

    # User Subscription functions

    def list_user_subscriptions(self, user_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/users/{user_id}/subscriptions.json' + option_string
        url = url.format(user_id=user_id)
        return self._page_gets(url, 'subscriptions')

    # Post Subscription functions

    def list_post_subscriptions(self, post_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/posts/{post_id}/subscriptions.json' + option_string
        url = url.format(post_id=post_id)
        return self._page_gets(url, 'subscriptions')

    def show_post_subscription(self, post_id, subscription_id):
        url = self.domain + '/api/v2/help_center/posts/{post_id}/subscriptions/{id}.json'.format(post_id=post_id, id=subscription_id)
        return self.get(url, self.email, self.password)

    def create_post_subscription(self, post_id, data):
        url = self.domain + '/api/v2/help_center/posts/{post_id}/subscriptions.json'.format(post_id=post_id)
        return self.post(url, data, self.email, self.password)

    def delete_post_subscription(self, post_id, subscription_id):
        url = self.domain + '/api/v2/help_center/posts/{post_id}/subscriptions/{id}.json'.format(post_id=post_id, id=subscription_id)
        return self.delete(url, self.email, self.password)

    # Topic Subscription functions

    def list_topic_subscriptions(self, topic_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/community/topics/{topic_id}/subscriptions.json' + option_string
        url = url.format(topic_id=topic_id)
        return self._page_gets(url, 'subscriptions')

    def show_topic_subscription(self, topic_id, subscription_id):
        url = self.domain + '/api/v2/community/topics/{topic_id}/subscriptions/{id}.json'.format(topic_id=topic_id, id=subscription_id)
        return self.get(url, self.email, self.password)

    def create_topic_subscription(self, topic_id, data):
        url = self.domain + '/api/v2/community/topics/{topic_id}/subscriptions.json'.format(topic_id=topic_id)
        return self.post(url, data, self.email, self.password)

    def delete_topic_subscription(self, topic_id, subscription_id):
        url = self.domain + '/api/v2/community/topics/{topic_id}/subscriptions/{id}.json'.format(topic_id=topic_id, id=subscription_id)
        return self.delete(url, self.email, self.password)

    # Vote functions

    def list_user_votes(self, user_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/users/{user_id}/votes.json' + option_string
        url = url.format(user_id=user_id)
        return self._page_gets(url, 'votes')

    def list_article_votes(self, article_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/votes.json' + option_string
        url = url.format(article_id=article_id)
        return self._page_gets(url, 'votes')

    def list_article_comment_votes(self, article_id, comment_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/articles/{article_id}/comments/{comment_id}/votes.json' + option_string
        url = url.format(article_id=article_id, comment_id=comment_id)
        return self._page_gets(url, 'votes')

    def list_post_votes(self, post_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/posts/{post_id}/votes.json' + option_string
        url = url.format(post_id=post_id)
        return self._page_gets(url, 'votes')

    def list_post_comment_votes(self, post_id, comment_id, options=None):
        option_string = self._generate_options(options)
        url = self.domain + '/api/v2/help_center/posts/{post_id}/comments/{comment_id}/votes.json' + option_string
        url = url.format(post_id=post_id, comment_id=comment_id)
        return self._page_gets(url, 'votes')

    def show_vote(self, vote_id):
        url = self.domain + '/api/v2/help_center/votes/{id}.json'.format(id=vote_id)
        return self.get(url, self.email, self.password)

    def vote_article_up(self, article_id):
        url = self.domain + '/api/v2/help_center/articles/{id}/up.json'.format(id=article_id)
        return self.post(url, self.email, self.password)

    def vote_article_down(self, article_id):
        url = self.domain + '/api/v2/help_center/articles/{id}/down.json'.format(id=article_id)
        return self.post(url, self.email, self.password)

    def vote_article_comment_up(self, article_id, comment_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/comments/{id}/up.json'.format(article_id=article_id, id=comment_id)
        return self.post(url, self.email, self.password)

    def vote_article_comment_down(self, article_id, comment_id):
        url = self.domain + '/api/v2/help_center/articles/{article_id}/comments/{id}/down.json'.format(article_id=article_id, id=comment_id)
        return self.post(url, self.email, self.password)

    def vote_post_up(self, post_id):
        url = self.domain + '/api/v2/help_center/posts/{id}/up.json'.format(id=post_id)
        return self.post(url, self.email, self.password)

    def vote_post_down(self, post_id):
        url = self.domain + '/api/v2/help_center/posts/{id}/down.json'.format(id=post_id)
        return self.post(url, self.email, self.password)

    def vote_post_comment_up(self, post_id, comment_id):
        url = self.domain + '/api/v2/help_center/posts/{post_id}/comments/{id}/up.json'.format(post_id=post_id, id=comment_id)
        return self.post(url, self.email, self.password)

    def vote_post_comment_down(self, post_id, comment_id):
        url = self.domain + '/api/v2/help_center/posts/{post_id}/comments/{id}/down.json'.format(post_id=post_id, id=comment_id)
        return self.post(url, self.email, self.password)

    def delete_vote(self, vote_id):
        url = self.domain + '/api/v2/help_center/votes/{id}.json'.format(id=vote_id)
        return self.delete(url, self.email, self.password)

    # Access policy functions

    def show_section_access_policy(self, section_id):
        url = self.domain + '/api/v2/help_center/sections/{section_id}/access_policy.json'.format(section_id=section_id)
        return self.get(url, self.email, self.password)

    def show_topic_access_policy(self, topic_id):
        url = self.domain + '/api/v2/community/topics/{topic_id}/access_policy.json'.format(topic_id=topic_id)
        return self.get(url, self.email, self.password)

    def update_section_access_policy(self, section_id, data):
        url = self.domain + '/api/v2/help_center/sections/{section_id}/access_policy.json'.format(section_id=section_id)
        return self.put(url, data, self.email, self.password)

    def update_topic_access_policy(self, topic_id, data):
        url = self.domain + '/api/v2/community/topics/{topic_id}/access_policy.json'.format(topic_id=topic_id)
        return self.put(url, data, self.email, self.password)

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
