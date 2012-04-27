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


class HTTPClientException(HTTPException):
    """Mixin class for the client errors 4xx.
    """

    def __init__(self, location):
        self.location = location


class HTTPBadRequest(HTTPClientException):
    code = 400
    title = 'Bad Request'


class HTTPUnauthorized(HTTPClientException):
    code = 401
    title = 'Unauthorized'


class HTTPayementRequired(HTTPClientException):
    code = 402
    title = 'PayementRequired'


class HTTPForbidden(HTTPClientException):
    code = 403
    title = 'HTTP Forbidden'


class HTTPNotFound(HTTPClientException):
    code = 404
    title = 'Not Found'


class HTTPMethodNotAllowed(HTTPClientException):
    code = 405
    title = 'Method Not Allowed'


class HTTPNotAcceptable(HTTPClientException):
    code = 406
    title = 'Not Acceptable'


class HTTPProxyAuthenticationRequired(HTTPClientException):
    code = 407
    title = 'Proxy Authentication Required'


class HTTPRequestTimeout(HTTPClientException):
    code = 408
    title = 'Request Timeout'


class HTTPConflict(HTTPClientException):
    code = 409
    title = 'Conflict'


class HTTPGone(HTTPClientException):
    code = 410
    title = 'Gone'


class HTTPLengthRequired(HTTPClientException):
    code = 411
    title = 'Length Required'


class HTTPPreconditionFailed(HTTPClientException):
    code = 412
    title = 'Precondition Failed'


class HTTPRequestEntityTooLarge(HTTPClientException):
    code = 413
    title = 'Request Entity Too Large'


class HTTPRequestURITooLong(HTTPClientException):
    code = 414
    title = 'Request-URI Too Long'


class HTTPUnsupportedMediaType(HTTPClientException):
    code = 415
    title = 'Unsupported Media Type'


class HTTPRequestedRangeNotSatisfiable(HTTPClientException):
    code = 416
    title = 'Requested Range Not Satisfiable'


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


CLIENT_ERRORS = {
    400: HTTPBadRequest,
    401: HTTPUnauthorized,
    402: HTTPayementRequired,
    403: HTTPForbidden,
    404: HTTPNotFound,
    405: HTTPMethodNotAllowed,
    406: HTTPNotAcceptable,
    407: HTTPProxyAuthenticationRequired,
    408: HTTPRequestTimeout,
    409: HTTPConflict,
    410: HTTPGone,
    411: HTTPLengthRequired,
    412: HTTPPreconditionFailed,
    413: HTTPRequestEntityTooLarge,
    414: HTTPRequestURITooLong,
    415: HTTPUnsupportedMediaType,
    416: HTTPRequestedRangeNotSatisfiable,
    }
