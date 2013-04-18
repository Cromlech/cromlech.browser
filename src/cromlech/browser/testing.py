# -*- coding: utf-8 -*-
"""tests helpers.
"""
import difflib
from BeautifulSoup import BeautifulStoneSoup
from cromlech.browser import IRequest, IResponse, IResponseFactory
from cromlech.browser import IView, IViewSlot, ILayout
from zope.interface import implementer


@implementer(IRequest)
class TestRequest(object):

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

        
@implementer(IResponse)
class TestResponse(object):

    body = ''
    charset = ''
    status = ''

    def __init__(self, status=None, charset=None, headers=None):
        self.headers = headers or {}
        self.charset = charset or 'UTF-8'
        self.status = status or '200 OK'

    @property
    def status_int(self):
        if self.status:
            return int(self.status[0:3])
        return None

    def write(self, data=None):
        """Writes data to the response.
        """
        self.body += data

    def __str__(self):
        return self.body

    def __iter__(self):
        return iter([self.body])

    def __call__(self, environ, start_response):
        start_response(self.status, self.headers.items())
        return iter(self)


@implementer(ILayout)
class TestLayout(object):
    """A trivial conformance to ILayout for testing.
    """

    def __call__(self, content, **env):
        raise NotImplementedError('You need to implement your own')


@implementer(IView, IResponseFactory)
class TestView(object):
    """A trivial conformance to IView for testing.
    """

    def __init__(self, context=None, request=None):
        self.context = context
        self.request = request

    def __call__(self):
        response = TestResponse()
        response.write(self.render())
        return response


@implementer(IViewSlot)
class TestViewSlot(object):
    """A trivial conformance to IViewSlot for testing.
    """

    def __init__(self, view):
        self.view = view

    def update(self):
        pass

    def render(self):
        return "%r is used" % self.view.__name__


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
