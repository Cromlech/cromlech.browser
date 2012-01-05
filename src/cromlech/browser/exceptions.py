# -*- coding: utf-8 -*-

from zope.interface import implements
from cromlech.browser.interfaces import IHTTPException, IHTTPRedirect


class HTTPException(Exception):
    implements(IHTTPException)
    code = None
    title = None


class HTTPRedirect(HTTPException):
    """Mixin class for the redirection exceptions.
    """
    implements(IHTTPRedirect)

    def __init__(self, location):
        self.location = location


class HTTPMultipleChoices(HTTPRedirect):
    code = 300
    title = 'Multiple Choices'


class HTTPMovedPermanently(HTTPRedirect):
    code = 301
    title = 'Moved Permanently'


class HTTPFound(HTTPRedirect):
    code = 302
    title = 'Found'


class HTTPSeeOther(HTTPRedirect):
    code = 303
    title = 'See Other'


class HTTPNotModified(HTTPRedirect):
    code = 304
    title = 'Not Modified'


class HTTPUseProxy(HTTPRedirect):
    code = 305
    title = 'Use Proxy'


class HTTPTemporaryRedirect(HTTPRedirect):
    code = 307
    title = 'Temporary Redirect'


class HTTPTooManyRedirect(HTTPRedirect):
    code = 310
    title = 'Too many Redirect'


REDIRECTIONS = {
    300: HTTPMultipleChoices,
    301: HTTPMovedPermanently,
    302: HTTPFound,
    303: HTTPSeeOther,
    304: HTTPNotModified,
    305: HTTPUseProxy,
    # 306 - Doesn't exist.
    307: HTTPTemporaryRedirect,
    310: HTTPTooManyRedirect,
    }
