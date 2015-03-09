Radric - Static website generator
=================================

Radric is a **static website generator** written in Python. Just write your pages and your posts in Markdown format, and Radric generates the HTML pages :

.. code-block::

    $ radric new-project mywebsite
    [*] New project created : /your/path/mywebsite
    $ cd mywebsite
    $ radric new-post "My first post"
    [*] New post created : /your/path/mywebsite/posts/my-first-post.md
    $ vim posts/my-first-post.md
    ...
    $ radric generate

The HTML pages will be accessible in the ``public`` folder.


Features
--------

- Posts and pages support
- Custom menu based on pages
- Categories, Tags and Authors management
- Drafts system
- Custom URLs structure
- Themes support
- Markdown edition
- Python 2 & Python 3

Notes
-----

Radric is in **Beta** version, a refactoring could appear in the future. The following features will also be added :

- RSS & Atom feeds
- An archives page
- The ReStructuredText support
- The pagination
- A search form in JS
- A plugin system
- Many themes
- ... and more !