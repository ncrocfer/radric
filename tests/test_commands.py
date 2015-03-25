# -*- coding: utf-8 -*-

import os
import re
import unittest
from testfixtures import log_capture

from radric.commands import Commands
from radric.exceptions import (PostExists,
                               PageExists)
from functions import (tmp_folder, capture, content_path,
                       create_project_structure,
                       POSTS_LIST, PAGES_LIST)


"""
class TotoTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
"""


class RadricCommandsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @log_capture()
    def test_new_no_blank_project(self, l):
        with tmp_folder() as tmp_dir:
            cmd = Commands({'<name>': 'test', '--blank': False})
            cmd.new_project()

            regex = re.compile(r"New project created : .*test$")
            self.assertTrue(regex.match(l.records[0].getMessage()))

            pages = [f for f in os.listdir(
                os.path.join(tmp_dir, "test", "pages"))
            ]
            posts = [f for f in os.listdir(
                os.path.join(tmp_dir, "test", "posts"))
            ]

            self.assertEqual(len(pages), 1)
            self.assertEqual(len(posts), 1)

    @log_capture()
    def test_new_blank_project(self, l):
        with tmp_folder() as tmp_dir:
            cmd = Commands({'<name>': 'test', '--blank': True})
            cmd.new_project()

            regex = re.compile(r"New project created : .*test$")
            self.assertTrue(regex.match(l.records[0].getMessage()))

            pages = [f for f in os.listdir(
                os.path.join(tmp_dir, "test", "pages"))
            ]
            posts = [f for f in os.listdir(
                os.path.join(tmp_dir, "test", "posts"))
            ]

            self.assertEqual(len(pages), 0)
            self.assertEqual(len(posts), 0)

    @log_capture()
    def test_new_post(self, l):
        with tmp_folder(project=True):
            cmd = Commands({'<name>': 'Hello World !'})
            cmd.new_post()

            regex = re.compile(r"New post created : .*hello-world.*")
            self.assertTrue(regex.match(l.records[0].getMessage()))

    @log_capture()
    def test_new_post_already_exists(self, l):
        with tmp_folder(project=True):
            cmd = Commands(
                {'<name>': 'Hello World !', '--force': False}
            )
            with self.assertRaises(PostExists):
                for _ in range(2):
                    cmd.new_post()

    @log_capture()
    def test_new_post_exits_with_force(self, l):
        with tmp_folder(project=True):
            cmd = Commands(
                {'<name>': 'Hello World !', '--force': True}
            )
            for _ in range(2):
                cmd.new_post()

            regex = re.compile(
                r"New post created : .*hello-world.*", re.DOTALL
            )
            self.assertTrue(regex.match(l.records[0].getMessage()))
            self.assertTrue(regex.match(l.records[1].getMessage()))

    @log_capture()
    def test_new_page(self, l):
        with tmp_folder(project=True):
            cmd = Commands({'<name>': 'A new page'})
            cmd.new_page()

            regex = re.compile(r"New page created : .*a-new-page.*")
            self.assertTrue(regex.match(l.records[0].getMessage()))

    @log_capture()
    def test_new_page_already_exists(self, l):
        with tmp_folder(project=True):
            cmd = Commands(
                {'<name>': 'A new page', '--force': False}
            )
            with self.assertRaises(PageExists):
                for _ in range(2):
                    cmd.new_page()

    @log_capture()
    def test_new_page_exits_with_force(self, l):
        with tmp_folder(project=True):
            cmd = Commands(
                {'<name>': 'A new page', '--force': True}
            )
            for _ in range(2):
                cmd.new_page()

            regex = re.compile(
                r"New page created : .*a-new-page.*", re.DOTALL
            )
            self.assertTrue(regex.match(l.records[0].getMessage()))
            self.assertTrue(regex.match(l.records[1].getMessage()))

    @log_capture()
    def test_generate_with_default(self, l):
        with tmp_folder(project=True):
            cmd = Commands({})
            cmd.generate()

            self.assertEqual(
                "Processed 1 post and 1 page",
                l.records[0].getMessage()
            )
            self.assertEqual(
                "0 draft remaining",
                l.records[1].getMessage()
            )

    @log_capture()
    def test_generate_with_drafted_posts(self, l):
        with tmp_folder(project=True):
            for post in POSTS_LIST.values():
                cmd = Commands({'<name>': post})
                cmd.new_post()
            cmd.generate()

            self.assertEqual(
                "Processed 1 post and 1 page",
                l.records[5].getMessage()
            )
            self.assertEqual(
                "5 drafts remaining",
                l.records[6].getMessage()
            )

    @log_capture()
    def test_generate_with_no_drafted_posts(self, l):
        with tmp_folder(project=True) as tmp_dir:
            with open(content_path('post_no_drafted.rst'), 'r') as f:
                content = f.read()
            for post in POSTS_LIST.keys():
                post_path = os.path.join(tmp_dir, 'posts', post)
                with open(post_path, "w") as f:
                    f.write(content)

            cmd = Commands({})
            cmd.generate()

            self.assertEqual(
                "Processed 6 posts and 1 page",
                l.records[0].getMessage()
            )
            self.assertEqual(
                "0 draft remaining",
                l.records[1].getMessage()
            )

    @log_capture()
    def test_generate_with_no_drafted_pages(self, l):
        with tmp_folder(project=True) as tmp_dir:
            with open(content_path('page_no_drafted.rst'), 'r') as f:
                content = f.read()
            for page in PAGES_LIST.keys():
                page_path = os.path.join(tmp_dir, 'pages', page)
                with open(page_path, "w") as f:
                    f.write(content)

            cmd = Commands({})
            cmd.generate()

            self.assertEqual(
                "Processed 1 post and 6 pages",
                l.records[0].getMessage()
            )
            self.assertEqual(
                "0 draft remaining",
                l.records[1].getMessage()
            )

    @log_capture()
    def test_no_tags_founds(self, l):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'empty_project')

            cmd = Commands({})
            cmd.tags()

            self.assertEqual(
                "No tags found.",
                l.records[0].getMessage()
            )

    @log_capture()
    def test_tag_not_found(self, l):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': 'Foo'})
            cmd.tags()

            self.assertEqual(
                "Tag 'Foo' not found.",
                l.records[0].getMessage()
            )

    def test_tag_found(self):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': None})
            with capture() as output:
                cmd.tags()

            regex = re.compile(r".*ExampleTag.*", re.DOTALL)
            self.assertTrue(regex.match(output[0]))

    def test_tag_detailed_found(self):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': 'ExampleTag'})
            with capture() as output:
                cmd.tags()

            regex = re.compile(r".*A post example.*", re.DOTALL)
            self.assertTrue(regex.match(output[0]))

    @log_capture()
    def test_no_categories_founds(self, l):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'empty_project')

            cmd = Commands({})
            cmd.categories()

            self.assertEqual(
                "No categories found.",
                l.records[0].getMessage()
            )

    @log_capture()
    def test_category_not_found(self, l):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': 'Foo'})
            cmd.categories()

            self.assertEqual(
                "Category 'Foo' not found.",
                l.records[0].getMessage()
            )

    def test_category_found(self):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': None})
            with capture() as output:
                cmd.categories()

            regex = re.compile(r".*ExampleCat.*", re.DOTALL)
            self.assertTrue(regex.match(output[0]))

    def test_category_detailed_found(self):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': 'ExampleCat'})
            with capture() as output:
                cmd.categories()

            regex = re.compile(r".*A post example.*", re.DOTALL)
            self.assertTrue(regex.match(output[0]))

    @log_capture()
    def test_no_authors_founds(self, l):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'empty_project')

            cmd = Commands({})
            cmd.authors()

            self.assertEqual(
                "No authors found.",
                l.records[0].getMessage()
            )

    @log_capture()
    def test_author_not_found(self, l):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': 'Foo'})
            cmd.authors()

            self.assertEqual(
                "Author 'Foo' not found.",
                l.records[0].getMessage()
            )

    def test_author_found(self):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': None})
            with capture() as output:
                cmd.authors()

            regex = re.compile(r".*John Doe \(john\).*", re.DOTALL)
            self.assertTrue(regex.match(output[0]))

    def test_author_detailed_found(self):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post')

            cmd = Commands({'<name>': 'john'})
            with capture() as output:
                cmd.authors()

            regex = re.compile(r".*A post example.*", re.DOTALL)
            self.assertTrue(regex.match(output[0]))

    @log_capture()
    def test_no_drafts_founds(self, l):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'empty_project')

            cmd = Commands({})
            cmd.drafts()

            self.assertEqual(
                "No drafts found.",
                l.records[0].getMessage()
            )

    def test_draft_found(self):
        with tmp_folder() as tmp_dir:
            create_project_structure(tmp_dir, 'one_post_drafted')

            cmd = Commands({})
            with capture() as output:
                cmd.drafts()

            regex = re.compile(r".*A draft example.*", re.DOTALL)
            self.assertTrue(regex.match(output[0]))
