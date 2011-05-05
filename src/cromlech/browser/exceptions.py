# -*- coding: utf-8 -*-

from zope.interface import implements
from cromlech.browser.interfaces import IHTTPException, IRedirect


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
