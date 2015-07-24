# -*- coding: utf-8 -*-

import os
import copy
import yaml
from datetime import datetime

from radric.exceptions import SettingsNotFoundException, YamlSyntaxException

DEFAULT_SETTINGS = {
    'SITE_URL': 'http://localhost:8000',
    'SITE_TITLE': 'Welcome in Radric',
    'SOURCE_PATH': '.',
    'DEFAULT_FORMAT': 'rst',
    'PUBLIC_FOLDER': 'public',
    'THEME': 'striped',
    'ASSETS_FOLDER': 'assets',
    'CSS_FILE': 'style.css',
    'CONTENT_DIRS': ['posts', 'pages'],
    'POST_FILE': 'post.html',
    'PAGE_FILE': 'page.html',
    'INDEX_FILE': 'index.html',
    'CATEGORY_FILE': 'category.html',
    'TAG_FILE': 'tag.html',
    'AUTHOR_FILE': 'author.html',
    'POST_URL': '{year}/{month}/{day}/{slug}.html',
    'PAGE_URL': '{slug}.html',
    'CATEGORY_URL': 'categories/{category}.html',
    'TAG_URL': 'tags/{tag}.html',
    'AUTHOR_URL': 'authors/{author}.html',
    'NOW': datetime.now(),
    'EXCERPT_SEPARATOR': '[--MORE--]'
}


class Settings(object):

    def __init__(self, args):
        self.args = args
        self.project_path = os.path.realpath(
            self.args.get('SOURCE_PATH', DEFAULT_SETTINGS['SOURCE_PATH'])
        )

    def merge_settings(self):
        merged_settings = copy.deepcopy(DEFAULT_SETTINGS)

        settings_path = os.path.join(self.project_path, 'settings.yml')

        try:
            settings_from_file = self.get_settings_from_file(settings_path)
        except IOError:
            raise SettingsNotFoundException(
                "File {} does not exist".format(settings_path)
            )
        except yaml.YAMLError:
            raise YamlSyntaxException(
                "Bad syntax of {}".format(settings_path)
            )

        settings_from_file.update(self.args)
        merged_settings.update(settings_from_file)

        merged_settings['SOURCE_PATH'] = self.project_path
        merged_settings['PUBLIC_FOLDER'] = os.path.join(
            self.project_path,
            merged_settings['PUBLIC_FOLDER']
        )

        return merged_settings

    def get_settings_from_file(self, path):
        settings = dict()

        with open(path, "r") as f:
            settings = f.read()

        settings = yaml.load(settings)
        settings = dict((k.upper(), v) for k, v in settings.items())

        return settings
