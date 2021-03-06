# -*- coding: utf-8 -*-

from .exceptions import REDIRECTIONS
from .interfaces import IHTTPRedirect, ILayout
from .directives import order
from zope.interface import implementer


def sort_components(components):
    """Sort a list of components using the information provided by
    `grok.order`.
    """
    def sort_key(component):
        value = order.get(component) or 0
        return (value, component.__module__, component.__class__.__name__)

    return sorted(components, key=sort_key)


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
    response_headers['Content-Length'] = '0'
    response_headers['Content-Type'] = 'text/plain'

    status = "%s %s" % (exception.code, exception.title)
    return responseFactory(status=status, headers=response_headers)


def redirect_exception_response(responseFactory, exception, **headers):
    if not IHTTPRedirect.providedBy(exception):
        raise RuntimeError('This is not a redirection')

    response_headers = {}
    if headers:
        response_headers.update(headers)
    response_headers['Location'] = exception.location
    response_headers['Content-Length'] = '0'
    response_headers['Content-Type'] = 'text/plain'

    status = "%s %s" % (exception.code, exception.title)
    return responseFactory(status=status, headers=response_headers)


@implementer(ILayout)
class HTMLWrapper(object):
    """HTMLWrapper is a base implementation of an `ILayout` component.
    The purpose is to provide a decoration for HTML content, destined
    to be rendered as standalone. It allows us to keep the template free
    of HTML base tags, in order to make it more likely to be reusable in
    another layout.
    """

    def __call__(self, content=u'', **kwargs):
        return u"<html><body>%s</body></html>" % content
