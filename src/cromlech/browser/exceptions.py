# -*- coding: utf-8 -*-

from zope.interface import implements
from cromlech.browser.interfaces import IHTTPException, IRedirect


REDIRECTION = {
    300: 'Multiple Choices',
    301: 'Moved Permanently',
    302: 'Found',
    303: 'See Other',
    304: 'Not Modified',
    305: 'Use Proxy',
    307: 'Temporary Redirect',
    310: 'Too many Redirect',
    }


class HTTPException(Exception):
    implements(IHTTPException)


class ResponseRedirect(HTTPException):
    implements(IRedirect)

    code = 303

    def __init__(self, location):
        self.location = location


class TemporaryRedirect(ResponseRedirect):
    code = 302


class PermanentRedirect(ResponseRedirect):
    code = 301
