# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute, implements


class IRenderer(Interface):
    """An object meant to render something.
    Most of the time, it gets an object and a request and returns
    a response.
    """

    def update(*args, **kwargs):
        """prepares the rendering
        """

    def render():
        """returns the raw data
        """

    def __call__():
        """returns a response object with the body and headers set.
        """


class IView(Interface):
    """Grok views all provide this interface."""

    context = Attribute('context', "Object that the view presents.")

    request = Attribute('request', "Request that the view was looked up with.")

    def __call__():
        """Returns a full Response object.
        """

    def update():
        """
        """

    def render():
        """
        """


class ISecuredItem(Interface):
    """
    """


class IViewlet(Interface):
    """
    """
