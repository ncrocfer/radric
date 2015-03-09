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
        self.content = None
        self.metas = {key: value for key, value in metas.items()}

        for key, value in self.metas.items():
            setattr(self, key, value)

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
