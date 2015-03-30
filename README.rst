Radric - Static website generator
=================================

Radric is a **static website generator** written in Python. Just write your pages and your posts in ReST or Markdown format, and Radric generates the HTML pages :

.. code-block::

    $ radric new-project mywebsite
    [*] New project created : /your/path/mywebsite
    $ cd mywebsite
    $ radric new-post "My first post"
    [*] New post created : /your/path/mywebsite/posts/my-first-post.rst
    $ vim posts/my-first-post.rst
    ...
    $ radric generate
    [*] Processed 1 post and 1 page
    [*] 0 draft remaining
    0.20 seconds

The HTML pages will be accessible in the ``public`` folder. You can view your website by launching the development server :

.. code-block::

    $ radric serve
    Serving HTTP on 0.0.0.0 port 8000 ...
    Use Control-C to exit


.. image:: https://raw.githubusercontent.com/ncrocfer/radric/master/radric.png
    :alt: Radric
    :width: 700
    :height: 382
    :align: center


Features
--------

- Posts and pages support
- ReST and Markdown formats
- Custom menu based on pages
- Categories, Tags and Authors management
- Drafts system
- Custom URLs structure
- A development server
- Themes support
- Markdown edition
- Python 2 & Python 3

Notes
-----

Radric is in **Beta** version, a refactoring could appear in the future. If you want to use a static generator in production, use the awesome `Pelican <http://blog.getpelican.com/>`_ project.

The following features will be added in the next releases:

- RSS & Atom feeds
- An archives page
- The pagination
- The code syntax highlighting
- A search form in JS
- A plugin system
- An import system (Wordpress, Joomla...)
- Many themes
- ... and more !
