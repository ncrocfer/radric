# -*- coding: utf-8 -*-

import os
import re
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from slugify import slugify


class Page(object):

    def __init__(self, path, metas, plaintext, settings):
        self.path = path
        self.plaintext = plaintext
        self.settings = settings
        self.content = None

        for key, value in metas.items():
            setattr(self, key, value)

    @property
    def slug(self):
        filename, _ = os.path.splitext(
            os.path.basename(self.path)
        )

        name = re.compile(r'(?P<slug>[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*)')
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
            '{slug}': self.slug
        }

        page_url = self.settings['PAGE_URL']
        for k, v in mapping.items():
            page_url = page_url.replace(k, v)

        return page_url
