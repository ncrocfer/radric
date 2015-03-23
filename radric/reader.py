# -*- coding: utf-8 -*-

import os


class Reader(object):

    def __init__(self, settings):
        self.settings = settings
        self.extensions = ['md', 'rst']
        self.files = dict()

    def get_files(self):
        if not self.files:
            files = dict()

            for dir in self.settings['CONTENT_DIRS']:
                files[dir] = []
                path = os.path.join(self.settings['SOURCE_PATH'], dir)

                for f in os.listdir(path):
                    if (os.path.isfile(os.path.join(path, f)) and
                            f.split('.')[-1] in self.extensions):
                        files[dir].append(os.path.join(path, f))

            self.files = files

        return self.files
