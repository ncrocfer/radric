# -*- coding: utf-8 -*-

import os
import sys
import distutils.core
from contextlib import contextmanager
from tempfile import mkdtemp
from shutil import rmtree
from six import StringIO
from datetime import datetime

from radric.utils import get_template_path


CURRENT_DIR = os.path.dirname(__file__)
CONTENT_PATH = os.path.join(CURRENT_DIR, 'content')

POSTS_LIST = {
    'a-new-post-1.md': 'A new post 1',
    'a-new-post-2.md': 'A new post 2',
    'a-new-post-3.md': 'A new post 3',
    'a-new-post-4.md': 'A new post 4',
    'a-new-post-5.md': 'A new post 5'
}

PAGES_LIST = {
    'a-new-page-1.md': 'A new page 1',
    'a-new-page-2.md': 'A new page 2',
    'a-new-page-3.md': 'A new page 3',
    'a-new-page-4.md': 'A new page 4',
    'a-new-page-5.md': 'A new page 5'
}

STRUCTURE = {
    'empty_project': ['pages', 'posts', 'public', 'settings.yml'],
    'one_page': ['posts', 'public', 'pages/about.md', 'settings.yml'],
    'one_post': ['pages', 'public', 'posts/post_no_drafted.md',
                 'settings.yml'],
    'one_post_drafted': ['pages', 'public', 'posts/post_drafted.md',
                         'settings.yml'],
}


def content_path(*args):
    return os.path.join(CONTENT_PATH, *args)


def create_project_structure(dst, structure):
    for path in STRUCTURE.get(structure, 'empty_project'):
        if "/" in path:
            dirs, file = os.path.split(path)
            try:
                os.makedirs(
                    os.path.join(dst, dirs)
                )
            except:
                raise

            if file:
                content = open(content_path(file)).read()
                with open(os.path.join(dst, path), "w") as f:
                    f.write(content)
        elif "." in path:
            content = open(content_path(path)).read()
            with open(os.path.join(dst, path), "w") as f:
                f.write(content)
        else:
            try:
                os.makedirs(
                    os.path.join(dst, path)
                )
            except:
                raise


@contextmanager
def tmp_folder(project=False):
    old_cwd = os.getcwd()
    tmp_dir = mkdtemp()
    os.chdir(tmp_dir)

    if project:
        template_path = get_template_path('project')
        distutils.dir_util.copy_tree(template_path, tmp_dir)

        old_post = os.path.join(
            tmp_dir,
            'posts',
            "welcome-to-radric.md"
        )

        now = datetime.now()
        with open(old_post, 'r+') as f:
            content = f.read()
            content = content.replace(
                'DATE',
                now.strftime('%Y-%m-%d %H:%M:%S')
            )

            f.seek(0)
            f.truncate()
            f.write(content)

        new_post = os.path.join(
            tmp_dir,
            'posts',
            "{}-welcome-to-radric.md".format(
                now.strftime('%Y-%m-%d')
            )
        )

        os.rename(old_post, new_post)

    try:
        yield tmp_dir
    finally:
        rmtree(tmp_dir)
        os.chdir(old_cwd)


@contextmanager
def capture():
    oldout, olderr = sys.stdout, sys.stderr
    try:
        out = [StringIO(), StringIO()]
        sys.stdout, sys.stderr = out
        yield out
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        out[0] = out[0].getvalue().strip()
        out[1] = out[1].getvalue().strip()
