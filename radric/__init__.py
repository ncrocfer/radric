# -*- coding: utf-8 -*-

"""Radric - A static website generator powered by Python

Usage:
  radric new-project <name> [--blank]
  radric new-post <name> [--path=<path>] [--force]
  radric new-page <name> [--path=<path>] [--force]
  radric generate [--path=<path>]
  radric tags [<name>] [--path=<path>]
  radric categories [<name>] [--path=<path>]
  radric authors [<name>] [--path=<path>]
  radric drafts [--path=<path>]
  radric serve [--port=<port>]
  radric (-h | --help)
  radric --version

Options:
  -h --help      Show this screen.
  --version      Show version.
  --blank        Creates an empty project.
  --force        Force creation even if the file already exists.
  --path=<path>  The project path.
  --port=<port>  The server port [default: 8000].
"""

from docopt import docopt
import time

from radric.commands import Commands
from radric.exceptions import RadricException
from radric.utils import init_logger

__version__ = "0.1"


class Radric(object):

    def __init__(self, arguments):
        self.args = arguments

    def run(self):
        mapping = {
            'generate': 'generate',
            'new-project': 'new_project',
            'new-post': 'new_post',
            'new-page': 'new_page',
            'tags': 'tags',
            'categories': 'categories',
            'drafts': 'drafts',
            'authors': 'authors',
            'serve': 'serve'
        }
        cmd = Commands(self.args)

        for a, c in mapping.items():
            if self.args[a]:
                start = time.time()
                try:
                    getattr(cmd, c)()
                except RadricException as e:
                    print("[!] {}".format(e))
                except Exception as e:
                    raise

                print("{:.2f} seconds".format(time.time() - start))


def main():
    arguments = docopt(__doc__, version=__version__)
    init_logger()

    radric = Radric(arguments)
    radric.run()
