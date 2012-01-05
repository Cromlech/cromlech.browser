# -*- coding: utf-8 -*-

from cromlech.browser.exceptions import REDIRECTIONS
from cromlech.browser.interfaces import IHTTPRedirect


def redirect_response(responseFactory, location, code=302, **headers):
    """Creates a redirect response.
    """
    exception = REDIRECTIONS.get(code)  # Get the exception class.
    if exception is None:
        raise RuntimeError('This is not a redirection')

    response_headers = {}
    if headers:
        response_headers.update(headers)
    response_headers['Location'] = location

    status = "%s %s" % (exception.code, exception.title)
    return responseFactory(status=status, headers=response_headers)


def redirect_exception_response(responseFactory, exception, **headers):
    if not IHTTPRedirect.providedBy(exception):
        raise RuntimeError('This is not a redirection')

    response_headers = {}
    if headers:
        response_headers.update(headers)
    response_headers['Location'] = exception.location

    status = "%s %s" % (exception.code, exception.title)
    return responseFactory(status=status, headers=response_headers)
