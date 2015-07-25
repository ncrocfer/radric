# -*- coding: utf-8 -*-

import os
import re
from slugify import slugify

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class Post(object):

    def __init__(self, path, metas, plaintext, settings):
        self.path = path
        self.plaintext = plaintext
        self.settings = settings
        self._content = None
        self._excerpt = None
        self._categories = list()
        self._tags = list()
        self.metas = {key: value for key, value in metas.items()}

        for key, value in self.metas.items():
            setattr(self, key, value)

    @property
    def content(self):
        if self.settings['EXCERPT_SEPARATOR'] in self._content:
            return self._content.replace(
                '<p>{}</p>'.format(self.settings['EXCERPT_SEPARATOR']),
                '',
                1
            )
        else:
            return self._content

    @content.setter
    def content(self, value):
        self._content = value

    @property
    def excerpt(self):
        if self._excerpt:
            return self._excerpt
        elif self.settings['EXCERPT_SEPARATOR'] in self._content:
            # return the excerpt without the <p>
            return self._content.split(
                self.settings['EXCERPT_SEPARATOR']
            )[0][:-3]
        else:
            return self._content

    @excerpt.setter
    def excerpt(self, value):
        self._excerpt = value

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, name):
        if type(name) is dict:
            self._categories.append(name)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, name):
        if type(name) is dict:
            self._tags.append(name)

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, name):
        if name in self.settings['AUTHORS']:
            self._author = self.settings['AUTHORS'][name]
        else:
            self._author = None

    @property
    def slug(self):
        filename, _ = os.path.splitext(
            os.path.basename(self.path)
        )

        name = re.compile(r'\d{4}(-\d{2}){2}-'
                          r'(?P<slug>[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*)')
        match = name.search(filename)

        if match:
            return match.group('slug')
        else:
            return slugify(self.title)

    @property
    def url(self):
        return urljoin(
            self.settings['SITE_URL'],
            self.folders
        )

    @property
    def folders(self):
        mapping = {
            '{year}': self.date.strftime('%Y'),
            '{month}': self.date.strftime('%m'),
            '{day}': self.date.strftime('%d'),
            '{slug}': self.slug
        }

        post_url = self.settings['POST_URL']
        for k, v in mapping.items():
            post_url = post_url.replace(k, v)

        return post_url
