# -*- coding: utf-8 -*-

import os
import unittest

from radric.utils import copy_project, get_template_path
from radric.exceptions import (TemplateNotFound,
                               DirectoryExistsException)
from functions import tmp_folder


class CopyDirTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_copy_no_empty_dir(self):
        project = get_template_path("project")
        with tmp_folder() as tmpdir:
            copy_project(project, os.path.join(tmpdir, "foo"), False)
            root = [f for f in os.listdir(
                os.path.join(tmpdir, "foo"))
            ]
            post = [f for f in os.listdir(
                os.path.join(tmpdir, "foo", "posts"))
            ]
            page = [f for f in os.listdir(
                os.path.join(tmpdir, "foo", "pages"))
            ]

            self.assertEqual(len(root), 5)
            self.assertEqual(len(post), 1)
            self.assertEqual(len(page), 1)

    def test_copy_empty_dir(self):
        project = get_template_path("project")
        with tmp_folder() as tmpdir:
            copy_project(project, os.path.join(tmpdir, "foo"), True)
            root = [f for f in os.listdir(
                os.path.join(tmpdir, "foo"))
            ]
            post = [f for f in os.listdir(
                os.path.join(tmpdir, "foo", "posts"))
            ]
            page = [f for f in os.listdir(
                os.path.join(tmpdir, "foo", "pages"))
            ]

            self.assertEqual(len(root), 5)
            self.assertEqual(len(post), 0)
            self.assertEqual(len(page), 0)

    def test_existing_dir(self):
        with tmp_folder() as tmpdir:
            with self.assertRaises(DirectoryExistsException):
                copy_project(tmpdir, tmpdir, False)


class TemplatePathTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_project_path(self):
        project = get_template_path("project")
        self.assertTrue(project.endswith('skeletons/project'))
        self.assertGreater(len([
            f
            for f in os.listdir(project)
        ]), 1)

    def test_post_path(self):
        post = get_template_path("post.rst")
        self.assertTrue(post.endswith('skeletons/post.rst'))

    def test_page_path(self):
        page = get_template_path("page.rst")
        self.assertTrue(page.endswith('skeletons/page.rst'))

    def test_return_template_not_found_exception(self):
        with self.assertRaises(TemplateNotFound):
            get_template_path('foo')
