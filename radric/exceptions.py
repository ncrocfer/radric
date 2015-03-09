# -*- coding: utf-8 -*-


class RadricException(Exception):
    pass


class SettingsNotFoundException(RadricException):
    pass


class YamlSyntaxException(RadricException):
    pass


class DirectoryExistsException(RadricException):
    pass


class OSException(RadricException):
    pass


class TemplateNotFound(RadricException):
    pass


class InvalidContentSyntax(RadricException):
    pass


class PostExists(RadricException):
    pass


class PageExists(RadricException):
    pass
