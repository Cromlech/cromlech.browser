# -*- coding: utf-8 -*-

from cromlech.io import IRequest, IResponse
from zope.interface import Interface, Attribute


class IHTTPRequest(IRequest):
    """A specialisation of an `IRequest`, defining a HTTP request.
    This kind of request is usually used by webservices, websites or
    other interoperable applications/components.
    """
    application_url = Attribute("Application URL.")
    body = Attribute("Body of the request.")
    charset = Attribute("Body of the request.")
    environment = Attribute("Environment of the request.")
    form = Attribute("Parsed GET or POST data.")
    method = Attribute("Method of the request.")
    script_name = Attribute("Name of the script root.")


class IHTTPResponse(IResponse):
    """A specialisation of an `IResponse`, defining a response in an HTTP
    context, most probably a response for a web browser request or such.
    """
    charset = Attribute("Body of the request.")
    headers = Attribute("headers of the response.")
    status = Attribute("Status including the code and the message.")


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


class ILayout(IRenderer):
    """A layout serves as a content decoration. Mainly used to maintain
    a site identity, it can be used as a simple renderer. Its `render`
    method uses the `content` argument as the content to be wrapped.
    """


class IHTTPRenderer(IRenderer):
    """A renderer returning an HTTPResponse
    """
    def __call__(*args, **kwargs):
        """Returns a response object with the body and headers set.
        """


class IView(IHTTPRenderer):
    """The view return content representation.
    Marker interface for a specialized http renderer.
    """


class IViewSlot(IRenderer):
    """A fragment of a view, acting as an aggregator of sub-renderers.
    """
    view = Attribute("Renderer on which the slot is called.")


class IForm(Interface):
    """Browser forms specific attributes"""

    postOnly = Attribute(
        u"Boolean indicating whether we only accept Post requests")
    formMethod = Attribute(u"Form method as a string")
    enctype = Attribute(u"Encoding type")


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


class ITraverser(Interface):
    """An interface to traverse using a namespace eg. ++mynamespace++myid
    """

    def traverse(namespace, identifier):
        """Do the traversing of namespace searching for identifier
        """


class IHTTPException(Interface):
    code = Attribute("Status code")
    title = Attribute("Status phrase. Eg: 'OK'")


class IHTTPRedirect(IHTTPException):
    location = Attribute("Location of the redirect.")
