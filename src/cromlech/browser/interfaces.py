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

    def render(*args, **kwargs):
        """Returns the raw data.
        """


class IHTTPRenderer(IRenderer):
    """A renderer returning an HTTPResponse
    """
    def __call__(*args, **kwargs):
        """Returns a response object with the body and headers set.
        """


class ILayout(IHTTPRenderer):
    """A layout renders common content of pages and place view and
    slot rendering inside
    """
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")


class IView(IHTTPRenderer):
    """The view return content representation
    """
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")
    response = Attribute("Response to be returned as a result of the call.")


class IViewSlot(IRenderer):
    """A fragment of a view, acting as an aggregator of sub-renderers.
    """
    context = Attribute("Object that the view presents.")
    request = Attribute("Request that the view was looked up with.")
    view = Attribute("Renderer on which the slot is called.")


class ITemplate(Interface):
    """a template
    """
    def render(component):
        """Renders the given component"""


class IURLResolver(Interface):
    """Component in charge of resolving an object into an URL.
    """
    def __str__():
        """Returns the URL of a component, if possible. Else, it
        raises a KeyError, precising what is missing for the resolution.
        """
