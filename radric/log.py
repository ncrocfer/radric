# -*- coding: utf-8 -*-

import logging


class RadricFormatter(logging.Formatter):

    error_fmt = "ERROR - %(msg)s"
    warning_fmt = "WARNING - %(msg)s"
    info_fmt = "[*] %(msg)s"
    debug_fmt = "DEBUG - %(module)s: %(lineno)d: %(msg)s"

    def __init__(self, fmt="[*] %(msg)s"):
        super(RadricFormatter, self).__init__(self, fmt)

    def format(self, record):
        format_orig = self._fmt

        if record.levelno == logging.DEBUG:
            self._fmt = RadricFormatter.debug_fmt

        elif record.levelno == logging.INFO:
            self._fmt = RadricFormatter.info_fmt

        elif record.levelno == logging.WARNING:
            self._fmt = RadricFormatter.warning_fmt

        elif record.levelno == logging.ERROR:
            self._fmt = RadricFormatter.error_fmt

        result = logging.Formatter.format(self, record)
        self._fmt = format_orig

        return result
