# -*- coding: utf-8 -*-
"""tests helpers"""

import sys
from BeautifulSoup import BeautifulStoneSoup
from cromlech.browser import IRenderer, IHTTPRenderer, IView, ILayout
from cromlech.io.testing.response import TestResponse
from optparse import OptionParser
from zope.interface import implements


class TestRenderer(object):
    """A trivial conformance to IRenderer for testing"""
    implements(IRenderer)

    def namespace(self):
        return dict()

    def update(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        return ""


class TestHTTPRenderer(TestRenderer):
    """A trivial conformance to IHTTPRenderer for testing"""
    implements(IHTTPRenderer)

    def __call__(self, *args, **kwargs):
        pass


class TestLayout(TestRenderer):
    """A trivial conformance to ILayout for testing"""
    implements(ILayout)

    def init(self, context=None, request=None):
        self.context = context
        self.request = request


class TestView(TestHTTPRenderer):
    """A trivial conformance to IView for testing"""
    implements(IView)

    responseFactory = TestResponse

    def init(self, context=None, request=None):
        self.context = context
        self.request = request


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
        return ['XML differ:\n-expected\n+actual\n',] + \
               list(difflib.unified_diff(
            pretty_xml1.splitlines(True),
            pretty_xml2.splitlines(True), n=2))[2:]
    return None
