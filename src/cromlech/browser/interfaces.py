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


class IHTTPRenderer(IRenderer):
    """
    """

    def __call__():
        """Returns a response object with the body and headers set.
        """


class ILayout(IHTTPRenderer):
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")


class IView(IHTTPRenderer):
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")


class IViewSlot(IRenderer):
    """A fragment of a view, acting as an aggregator of sub-renderers.
    """
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")
    view = Attribute("Renderer on which the slot is called.")
