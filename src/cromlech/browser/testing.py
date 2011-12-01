# -*- coding: utf-8 -*-
"""tests helpers.
"""
import difflib
from BeautifulSoup import BeautifulStoneSoup
from cromlech.browser import IHTTPRenderer, IHTTPRequest, IHTTPResponse
from cromlech.browser import IRenderer, IView, ILayout
from zope.interface import implements


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


class TestHTTPRequest(object):
    implements(IHTTPRequest)

    form = {}
    body = ''
    application_url = 'http://localhost'
    method = 'GET'
    charset = 'UTF-8'
    script_name = ''

    def __init__(self, form=None, environment=None, path='/', **kw):
        if environment is None:
            environment = {}

        if form is None:
            form = {}

        self.body = ''
        self.form = form
        self.script_name = ''
        self.environment = environment
        self.path = path
        self.__dict__.update(kw)


class TestHTTPResponse(object):
    implements(IHTTPResponse)

    charset = ''
    status_int = 200
    status = '200 - OK'
    body = ''

    def __init__(self, charset=None, headers=None):
        self.headers = headers or {}
        self.charset = charset or 'UTF-8'

    def redirect(self, url, status=302, trusted=False):
        """Sets the response for a redirect.
        """
        if not status in REDIRECTION:
            raise NotImplementedError('This is not a redirection')

        self.status_int = status
        self.status = "%s - %s" % (status, REDIRECTION[status])
        self.headers['Location'] = url

    def write(self, data=None):
        """Writes data to the response.
        """
        self.body += data

    def __str__(self):
        return self.body

    def __iter__(self):
        return iter([self.body])


class TestRenderer(object):
    """A trivial conformance to IRenderer for testing.
    """
    implements(IRenderer)

    def namespace(self):
        return dict()

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        return ""


class TestHTTPRenderer(TestRenderer):
    """A trivial conformance to IHTTPRenderer for testing.
    """
    implements(IHTTPRenderer)

    def __call__(self, *args, **kwargs):
        pass


class TestLayout(TestHTTPRenderer):
    """A trivial conformance to ILayout for testing.
    """
    implements(ILayout)

    def __init__(self, context=None, request=None):
        self.context = context
        self.request = request


class TestView(TestHTTPRenderer):
    """A trivial conformance to IView for testing.
    """
    implements(IView)

    response = None
    responseFactory = TestHTTPResponse

    def __init__(self, context=None, request=None):
        self.context = context
        self.request = request

    def update(self, *args, **kwargs):
        self.response = self.responseFactory()

    def render(self, *args, **kwargs):
        raise NotImplementedError('You need to implement your own')

    def __call__(self, *args, **kwargs):
        self.update()
        self.response.write(self.render())
        return self.response


class XMLSoup(BeautifulStoneSoup):

    def _smartPop(self, name):
        """We don't want to 'clean' the DOM.
        """
        pass


def XMLDiff(xml1, xml2):
    """Assert that two XML content are the same, or fail with a
    comprehensive diff between them.

    You should not use this if you which to compare XML data where
    spaces does matter.
    """
    pretty_xml1 = XMLSoup(xml1.strip()).prettify()
    pretty_xml2 = XMLSoup(xml2.strip()).prettify()
    if pretty_xml1 != pretty_xml2:
        return (['XML differ:\n-expected\n+actual\n'] +
                list(difflib.unified_diff(
                    pretty_xml1.splitlines(True),
                    pretty_xml2.splitlines(True), n=2))[2:])
    return None
