# -*- coding: utf-8 -*-

import shutil
import os
import logging
from datetime import datetime

from radric.log import RadricFormatter
from radric.exceptions import (DirectoryExistsException, OSException,
                               TemplateNotFound)


def copy_project(src, dst, blank):
    if os.path.isdir(dst):
        raise DirectoryExistsException(
            "Directory {} already exists".format(dst)
        )

    now = datetime.now()

    try:
        ignored = None
        if blank:
            ignored = shutil.ignore_patterns('*.rst')

        shutil.copytree(src, dst, ignore=ignored)

        if not blank:
            old_post = os.path.join(
                dst,
                'posts',
                "welcome-to-radric.rst"
            )

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
                dst,
                'posts',
                "{}-welcome-to-radric.rst".format(
                    now.strftime('%Y-%m-%d')
                )
            )

            os.rename(old_post, new_post)

    except OSError as exc:
        raise OSException(exc)


def get_template_path(template):
    skeletons_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'skeletons'
    )

    tpl_allowed = ['project', 'post.rst', 'page.rst']

    if template not in tpl_allowed:
        raise TemplateNotFound("{} template not found".format(template))

    return os.path.join(
        skeletons_path,
        template
    )


def init_logger():
    formatter = RadricFormatter()
    handler = logging.StreamHandler()
    logger = logging.getLogger()

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
