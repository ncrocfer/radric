# -*- coding: utf-8 -*-

import re
import os
import yaml
import logging
from markdown import markdown
from slugify import slugify
from jinja2 import Environment, FileSystemLoader
from docutils.core import publish_parts

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from radric.post import Post
from radric.page import Page
from radric.exceptions import InvalidContentSyntax, FormatException


logger = logging.getLogger()


class BaseGenerator(object):

    def __init__(self, settings, context):
        self.settings = settings
        self.context = context
        theme_path = os.path.join(
            self.settings['SOURCE_PATH'],
            'themes',
            self.settings['THEME']
        )
        self.env = Environment(loader=FileSystemLoader(theme_path))

    def extract_meta(self, content):
        r = re.compile('---(.*?)---(.*)', re.DOTALL)
        src = r.search(content)

        if not src:
            raise InvalidContentSyntax()

        metas = {}
        metas = yaml.load(src.group(1))

        return metas, src.group(2)

    def generate_html(self, file):
        name, ext = os.path.splitext(file.path)

        if 'rst' in ext:
            parts = publish_parts(file.plaintext, writer_name='html')
            return parts['fragment']
        elif 'md' in ext:
            return markdown(file.plaintext)
        else:
            raise FormatException()


class PostsGenerator(BaseGenerator):

    def __init__(self, *args, **kwargs):
        self.posts = list()
        self.drafts = list()
        self.categories = dict()
        self.tags = dict()
        self.authors = dict()
        super(PostsGenerator, self).__init__(*args, **kwargs)

    def process(self, reader):
        files = reader.get_files()

        for post_path in files['posts']:
            with open(post_path, "r") as f:

                try:
                    metas, plaintext = self.extract_meta(f.read())
                except InvalidContentSyntax:
                    logger.error(
                        "Bad syntax for {} file (skip it)".format(post_path)
                    )
                    continue

                p = Post(
                    path=post_path,
                    metas=metas,
                    plaintext=plaintext,
                    settings=self.settings
                )

                if 'draft' in metas and metas['draft']:
                    self.drafts.append(p)
                    continue

                self.posts.append(p)

                # Categories
                if 'categories' in metas:
                    for cat in metas['categories']:
                        if cat not in self.categories:
                            url = self.settings['CATEGORY_URL'].replace(
                                '{category}',
                                slugify(cat)
                            )
                            self.categories[cat] = dict()
                            self.categories[cat]['name'] = cat
                            self.categories[cat]['folders'] = url
                            self.categories[cat]['url'] = urljoin(
                                self.settings['SITE_URL'],
                                self.categories[cat]['folders']
                            )
                            self.categories[cat]['posts'] = list()

                        self.categories[cat]['posts'].append(p)

                # Tags
                if 'tags' in metas:
                    for tag in metas['tags']:
                        if tag not in self.tags:
                            url = self.settings['TAG_URL'].replace(
                                '{tag}',
                                slugify(tag)
                            )
                            self.tags[tag] = dict()
                            self.tags[tag]['name'] = tag
                            self.tags[tag]['folders'] = url
                            self.tags[tag]['url'] = urljoin(
                                self.settings['SITE_URL'],
                                self.tags[tag]['folders']
                            )
                            self.tags[tag]['posts'] = list()

                        self.tags[tag]['posts'].append(p)

                # Authors
                if 'author' in metas:
                    if metas['author'] in self.settings['AUTHORS']:

                        author = metas['author']
                        if author not in self.authors:
                            url = self.settings['AUTHOR_URL'].replace(
                                '{author}',
                                author
                            )
                            self.authors[author] = self.settings['AUTHORS'] \
                                                       .get(metas['author'])
                            self.authors[author]['slug'] = author
                            self.authors[author]['folders'] = url
                            self.authors[author]['url'] = urljoin(
                                self.settings['SITE_URL'],
                                self.authors[author]['folders']
                            )
                            self.authors[author]['posts'] = list()

                        self.authors[author]['posts'].append(p)

        self.context['categories'] = self.categories = self.categories.values()
        self.context['tags'] = self.tags = self.tags.values()
        self.context['authors'] = self.authors = self.authors.values()
        self.context['posts'] = self.posts

        return self

    def generate(self, writer, context):
        for post in self.posts:
            self.generate_post(writer, context, post)

        for category in self.categories:
            self.generate_category(writer, context, category)

        for tag in self.tags:
            self.generate_tag(writer, context, tag)

        for author in self.authors:
            self.generate_author(writer, context, author)

        self.generate_index(writer, context)

    def generate_category(self, writer, context, category):
        template = self.env.get_template(self.settings['CATEGORY_FILE'])
        context['category'] = category
        content = template.render(**context).encode('utf-8')

        endpoint = writer.create_folders(category['folders'])
        writer.write(endpoint, content)

    def generate_tag(self, writer, context, tag):
        template = self.env.get_template(self.settings['TAG_FILE'])
        context['tag'] = tag
        content = template.render(**context).encode('utf-8')

        endpoint = writer.create_folders(tag['folders'])
        writer.write(endpoint, content)

    def generate_author(self, writer, context, author):
        template = self.env.get_template(self.settings['AUTHOR_FILE'])
        context['author'] = author
        content = template.render(**context).encode('utf-8')

        endpoint = writer.create_folders(author['folders'])
        writer.write(endpoint, content)

    def generate_post(self, writer, context, post):
        template = self.env.get_template(self.settings['POST_FILE'])
        html = self.generate_html(post)
        post.content = html

        context['post'] = post
        content = template.render(**context).encode('utf-8')

        endpoint = writer.create_folders(post.folders)
        writer.write(endpoint, content)

    def generate_index(self, writer, context):
        index_path = os.path.join(
            self.settings['SOURCE_PATH'],
            self.settings['PUBLIC_FOLDER'],
            'index.html'
        )

        template = self.env.get_template(self.settings['INDEX_FILE'])
        content = template.render(**context).encode('utf-8')

        writer.write(index_path, content)


class PagesGenerator(BaseGenerator):

    def __init__(self, *args, **kwargs):
        self.pages = list()
        self.drafts = list()
        super(PagesGenerator, self).__init__(*args, **kwargs)

    def process(self, reader):
        files = reader.get_files()

        for page_path in files['pages']:
            with open(page_path, "r") as f:

                try:
                    metas, plaintext = self.extract_meta(f.read())
                except InvalidContentSyntax:
                    logger.error(
                        "Bad syntax for {} file (skip it)".format(page_path)
                    )
                    continue

                page = Page(
                    path=page_path,
                    metas=metas,
                    plaintext=plaintext,
                    settings=self.settings
                )

                if 'draft' in metas and metas['draft']:
                    self.drafts.append(page)
                    continue

                self.pages.append(page)

        self.context['pages'] = self.pages

        return self

    def generate(self, writer, context):
        for page in self.pages:
            self.generate_page(writer, context, page)

    def generate_page(self, writer, context, page):
        template = self.env.get_template(self.settings['PAGE_FILE'])
        html = self.generate_html(page)
        page.content = html
        context['page'] = page

        content = template.render(**context).encode('utf-8')

        endpoint = writer.create_folders(page.folders)
        writer.write(endpoint, content)
