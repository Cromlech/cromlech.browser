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


class IBaseClasses(Interface):
    View = Attribute("Base class for browser views.")


class IDirectives(Interface):

    def request(interface):
        """Define on which request a component is registered.
        This can be used to narrow to a skin type.
        """

    def view(view):
        """Define on which view a viewlet manager/viewlet is registered.
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
