# -*- coding: utf-8 -*-

import os
import shutil

from radric.exceptions import OSException


class Writer(object):

    def __init__(self, settings):
        self.settings = settings

    def write(self, file, content):
        with open(file, 'wb') as fw:
            fw.write(content)

    def create_folders(self, url):
        folders = url.rstrip('/').split('/')

        endpoint = 'index.html'
        if folders[-1].endswith('.html'):
            endpoint = folders[-1]
            folders.pop()

        folders_path = os.path.join(
            self.settings['SOURCE_PATH'],
            self.settings['PUBLIC_FOLDER'],
            "/".join(folders)
        )

        if not os.path.exists(folders_path):
            os.makedirs(folders_path)

        return os.path.join(folders_path, endpoint)

    def copy_assets(self, src=None, dst=None):
        if not src:
            src = os.path.join(
                self.settings['SOURCE_PATH'],
                'themes',
                self.settings['THEME'],
                self.settings['ASSETS_FOLDER']
            )

        if not dst:
            dst = os.path.join(
                self.settings['SOURCE_PATH'],
                self.settings['PUBLIC_FOLDER']
            )

        if not os.path.exists(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            if os.path.isdir(s):
                self.copy_assets(s, d)
            else:
                shutil.copy2(s, d)

    def copy_static_folders(self, dst=None):

        folders = self.settings.get('STATIC_DIRS', [])

        for dir in folders:
            src = os.path.join(
                self.settings['SOURCE_PATH'],
                dir
            )

            if not dst:
                dst = os.path.join(
                    self.settings['SOURCE_PATH'],
                    self.settings['PUBLIC_FOLDER'],
                    dir
                )

            try:
                shutil.rmtree(dst, ignore_errors=True)
                shutil.copytree(src, dst)
            except OSError:
                raise OSException("Unable to copy the static folders.")
