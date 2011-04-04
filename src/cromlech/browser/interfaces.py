# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute


class IRenderer(Interface):
    """An object meant to render something.
    
    Most of the time, it gets an object and a request and returns
    a response but may also return raw data.
    """
    def namespace():
        """A dict representing the values accessible by the templates.
        """

    def update(*args, **kwargs):
        """Prepares the rendering.
        """

    def render():
        """Returns the raw data.
        """


class ILayout(IRenderer):
    """Global layout view.
    """


class IView(IRenderer):
    """Grok views all provide this interface.
    """

    context = Attribute('context', "Object that the view presents.")
    request = Attribute('request', "Request that the view was looked up with.")

    def __call__():
        """Returns a response object with the body and headers set.
        """
