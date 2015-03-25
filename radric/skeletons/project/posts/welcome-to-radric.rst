---
title: Welcome to Radric
date: DATE
author: radric
categories: ["Examples"]
tags: ["radric"]
---

If you see this first post, **you have successfully created a new project** !

You can now delete this post and start creating others :

::

    $ radric new-post "My first post"
    $ vim posts/my-first-post.rst
    ...
    $ radric generate
    $ cd public
    $ python -m "SimpleHTTPServer" # or http.server for Python 3
    Serving HTTP on 0.0.0.0 port 8000 ...

Radric accepts the `ReST`_ and the `Markdown`_ formats.

It also provides some help to manage :

-  your pages (with the ``new-page`` command)
-  your post categories (``categories`` command)
-  your post tags (``tags`` command)
-  your URL structure
-  your menu items
-  your themes

For now, Radric is in **Beta** version. To get more information, have a look at the `documentation`_.

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _ReST: http://docutils.sourceforge.net/rst.html
.. _documentation: https://github.com/ncrocfer/radric/wiki