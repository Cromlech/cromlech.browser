"""tests helpers"""


from zope.interface import implements
from interfaces import IRenderer, IHTTPRenderer, IView, ILayout


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


class TestView(TestHTTPRenderer):
    """A trivial conformance to IView for testing"""
    implements(IView)

    response = None

    def init(self, context=None, request=None):
        self.context = context
        self.request = request


class TestLayout(TestRenderer):
    """A trivial conformance to ILayout for testing"""
    implements(ILayout)

    def init(self, context=None, request=None):
        self.context = context
        self.request = request
