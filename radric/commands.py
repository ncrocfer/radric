# -*- coding: utf-8 -*-

import os
import six
from slugify import slugify
from datetime import datetime
import logging
from prettytable import PrettyTable

from radric.reader import Reader
from radric.writer import Writer
from radric.settings import Settings
from radric.generators import PostsGenerator, PagesGenerator
from radric.utils import copy_project, get_template_path
from radric.exceptions import PostExists, PageExists

if six.PY3:
    import http.server
    import socketserver
else:
    import BaseHTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler


logger = logging.getLogger()


class Commands(object):

    def __init__(self, args):
        self.args = args
        self.context = {}

    def new_project(self):
        template_path = get_template_path('project')
        project_path = os.path.realpath(self.args['<name>'])

        copy_project(
            template_path,
            project_path,
            self.args['--blank']
        )

        logger.info("New project created : {}".format(project_path))

    def new_post(self):
        settings = self._get_settings()
        template_file = 'post.{}'.format(settings['DEFAULT_FORMAT'])
        template_path = get_template_path(template_file)

        with open(template_path, "r") as f:
            content = f.read()

            slug = slugify(self.args['<name>'])
            now = datetime.now()

            content = content.replace('TITLE', self.args['<name>'])
            content = content.replace(
                'DATE',
                now.strftime('%Y-%m-%d %H:%M:%S')
            )

        post_path = os.path.join(
            settings['SOURCE_PATH'],
            'posts',
            '{}-{}.{}'.format(now.strftime('%Y-%m-%d'), slug, settings['DEFAULT_FORMAT'])
        )

        if (os.path.isfile(post_path) and
                not self.args['--force']):
            raise PostExists(
                "The post '{}' already exists (use --force).".format(post_path)
            )

        with open(post_path, "w") as f:
            f.write(content)

        logger.info("New post created : {}".format(post_path))

    def new_page(self):
        settings = self._get_settings()
        template_file = 'page.{}'.format(settings['DEFAULT_FORMAT'])
        template_path = get_template_path(template_file)

        with open(template_path, "r") as f:
            content = f.read()

            slug = slugify(self.args['<name>'])
            content = content.replace('TITLE', self.args['<name>'])

        page_path = os.path.join(
            settings['SOURCE_PATH'],
            'pages',
            '{}.{}'.format(slug, settings['DEFAULT_FORMAT'])
        )

        if (os.path.isfile(page_path) and
                not self.args['--force']):
            raise PageExists(
                "The page '{}' already exists (use --force).".format(page_path)
            )

        with open(page_path, "w") as f:
            f.write(content)

        logger.info("New page created : {}".format(page_path))

    def generate(self):
        settings = self._get_settings()
        reader = Reader(settings)
        writer = Writer(settings)

        self.context = settings.copy()
        generators = [
            cls(settings, self.context)
            for cls in [PostsGenerator, PagesGenerator]
        ]

        for generator in generators:
            g = generator.process(reader)
            self.context.update(g.context)

        for generator in generators:
            generator.generate(writer, self.context)

            if hasattr(generator, 'posts'):
                posts = generator.posts
                posts_drafts = generator.drafts

            if hasattr(generator, 'pages'):
                pages = generator.pages
                page_drafts = generator.drafts

        writer.copy_assets()

        logger.info("Processed {0} post{1} and {2} page{3}".format(
            len(posts),
            "s"[len(posts) <= 1:],
            len(pages),
            "s"[len(pages) <= 1:]
        ))

        logger.info("{0} draft{1} remaining".format(
            len(posts_drafts) + len(page_drafts),
            "s"[len(posts_drafts) + len(page_drafts) <= 1:]
        ))

    def tags(self):
        settings = self._get_settings()
        reader = Reader(settings)

        generator = PostsGenerator(settings, self.context).process(reader)

        if not generator.tags:
            logger.info("No tags found.")
            return

        if not self.args['<name>']:
            table = PrettyTable(["Tags", "Posts"])
            table.align["Tags"] = "l"

            for tag in generator.tags:
                table.add_row([tag['name'], len(tag['posts'])])

            print(table.get_string(sortby="Posts", reversesort=True))

        else:
            tag = (item
                   for item in generator.tags
                   if item['name'] == self.args['<name>'])
            tag = next(tag, None)

            if not tag:
                logger.info(
                    "Tag '{}' not found.".format(self.args['<name>'])
                )
                return

            table = PrettyTable(["Posts", "Date", "Tags"])
            table.align["Posts"] = "l"

            for post in tag['posts']:
                tags = [t['name'] for t in post.tags]
                table.add_row([
                    post.title,
                    post.date.strftime("%B %d, %Y"),
                    ", ".join(tags)
                ])

            print(table.get_string(sortby="Date", reversesort=True))

    def categories(self):
        settings = self._get_settings()
        reader = Reader(settings)

        generator = PostsGenerator(settings, self.context).process(reader)

        if not generator.categories:
            logger.info("No categories found.")
            return

        if not self.args['<name>']:
            table = PrettyTable(["Categories", "Posts"])
            table.align["Categories"] = "l"

            for category in generator.categories:
                table.add_row([category['name'], len(category['posts'])])

            print(table.get_string(sortby="Posts", reversesort=True))

        else:
            category = (item
                        for item in generator.categories
                        if item['name'] == self.args['<name>'])
            category = next(category, None)

            if not category:
                logger.info(
                    "Category '{}' not found.".format(self.args['<name>'])
                )
                return

            table = PrettyTable(["Posts", "Date", "Categories"])
            table.align["Posts"] = "l"

            for post in category['posts']:
                categories = [c['name'] for c in post.categories]
                table.add_row([
                    post.title,
                    post.date.strftime("%B %d, %Y"),
                    ", ".join(categories)
                ])

            print(table.get_string(sortby="Date", reversesort=True))

    def drafts(self):
        settings = self._get_settings()

        reader = Reader(settings)

        posts = PostsGenerator(settings, self.context).process(reader)
        pages = PagesGenerator(settings, self.context).process(reader)

        drafts = posts.drafts + pages.drafts

        if not drafts:
            logger.info("No drafts found.")
            return

        table = PrettyTable(["Type", "Title"])
        table.align["Type"] = "l"

        for draft in drafts:
            table.add_row([
                draft.__class__.__name__,
                draft.title
            ])

        print(table.get_string(sortby="Type"))

    def authors(self):
        settings = self._get_settings()
        reader = Reader(settings)

        generator = PostsGenerator(settings, self.context).process(reader)

        if not generator.authors:
            logger.info("No authors found.")
            return

        if not self.args['<name>']:
            table = PrettyTable(["Authors", "Posts"])
            table.align["Authors"] = "l"

            for author in generator.authors:
                table.add_row([
                    "{} ({})".format(author['name'], author['slug']),
                    len(author['posts'])
                ])

            print(table.get_string(sortby="Posts", reversesort=True))

        else:
            author = (item
                      for item in generator.authors
                      if item['slug'] == self.args['<name>'])
            author = next(author, None)

            if not author:
                logger.info(
                    "Author '{}' not found.".format(self.args['<name>'])
                )
                return

            table = PrettyTable(["Posts", "Date"])
            table.align["Posts"] = "l"

            for post in author['posts']:
                table.add_row([
                    post.title,
                    post.date.strftime("%B %d, %Y")
                ])

            print(table.get_string(sortby="Date", reversesort=True))

    def serve(self):
        settings = self._get_settings()
        port = int(self.args['--port'])
        os.chdir(settings['PUBLIC_FOLDER'])

        if six.PY3:
            Handler = http.server.SimpleHTTPRequestHandler
            httpd = socketserver.TCPServer(("127.0.0.1", port), Handler)
        else:
            HandlerClass = SimpleHTTPRequestHandler
            ServerClass = BaseHTTPServer.HTTPServer
            Protocol = "HTTP/1.0"
            server_address = ('127.0.0.1', port)
            HandlerClass.protocol_version = Protocol
            httpd = ServerClass(server_address, HandlerClass)

        print("Serving HTTP on 0.0.0.0 port {} ...".format(port))
        print("Use Control-C to exit")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            exit("Bye :)")
        finally:
            os.chdir(settings['SOURCE_PATH'])

    def _get_settings(self):
        ARGS = dict()
        if('--path' in self.args and self.args['--path']):
            ARGS['SOURCE_PATH'] = self.args['--path']

        settings = Settings(ARGS).merge_settings()
        return settings
