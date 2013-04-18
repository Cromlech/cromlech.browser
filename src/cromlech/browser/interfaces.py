
# -*- coding: utf-8 -*-

from zope.interface import Attribute, Interface, implementer, moduleProvides
from zope.interface.common.mapping import IMapping


class ISession(IMapping):
    """A session mapping, used to handle session datas.
    """
    pass


class IRequest(Interface):
    """A request represents the application input medium: the HTTP request.
    This kind of request is usually used by webservices, websites or
    other interoperable applications/components.
    """
    application_url = Attribute("Application URL.")
    body = Attribute("Body of the request.")
    charset = Attribute("Body of the request.")
    environment = Attribute("Environment of the request.")
    form = Attribute("Parsed GET or POST data.")
    method = Attribute("Method of the request.")
    path = Attribute("Requested path of the resource (URI)")
    script_name = Attribute("Name of the script root.")


class ITypedRequest(IRequest):
    """Base interface for typed http request interfaces
    """


class IWSGIComponent(Interface):
    """Defines a component that is able to respond to a direct WSGI Call.
    More widely, this defines the very basics of a WSGI Application.
    """

    def __call__(environ, start_response):
        """Cooks a valid WSGI response thanks to start_response,
        setting headers and returning an iterable body.
        """


class IResponse(IWSGIComponent):
    """A response is the actor responding to the request. The request being
    the input, the response is the output. It has a result code and a body.
    A conveniant method `write` allows us to interact with the body.
    """
    headers = Attribute("headers of the response.")
    status = Attribute("Status including the code and the message.")
    body = Attribute("Body of the response.")
    charset = Attribute("Charset used in the body.")

    def write(data):
        """Writes data to the response's body.
        """


class IResponseFactory(Interface):
    """A response factory.
    """

    def __call__():
        """Returns a IResponse object.
        """


class IView(Interface):
    """Indicates that a component is a view.

    The publisher tries to adapt the context and request
    to an IView. After this, the publisher will try to
    adapt the resulting IView to IResponseFactory.

    The component that implements this interface will therefore have
    to implement IResponseFactory or alternatively an adapter should
    exist that knows how to convert this component to an IResponseFactory.
    """


class IRenderable(Interface):
    """A view-like object that uses a two-phase strategy for rendering.

    When a renderable is rendered, first the update method is called
    to prepare it for rendering. After this, the render method is used
    to actually render the view. The render method returns either a
    unicode string with the rendered content, or an IResponse object.
    """

    def update():
        """Prepares the rendering.
        """

    def render():
        """Returns the raw data.
        """


class ISlot(Interface):
    """A group-like item that acts like a components' hub.
    """


class IViewSlot(ISlot, IRenderable):
    """A fragment of a view, acting as an aggregator of sub-renderers.
    """
    view = Attribute("Renderer on which the slot is called.")


class ILayout(Interface):
    """A layout serves as a content decoration. Mainly used to maintain
    a site identity, it can be used as a simple renderer. Its `render`
    method uses the `content` argument as the content to be wrapped.
    """

    def __call__(content, **layout_environ):
        """Wraps the content into a 'decoration'. The `layout_environ`
        dict can contain additional data helping to render this component.
        """


class IForm(Interface):
    """Forms specific attributes.
    """
    postOnly = Attribute(
        u"Boolean indicating whether we only accept Post requests")
    formMethod = Attribute(u"Form method as a string")
    enctype = Attribute(u"Encoding type")


class ITemplate(Interface):
    """a template
    """

    def render(component, translate=None, **namespace):
        """Renders the given component.
        """


class IURL(Interface):
    """Component in charge of computing and object URL.
    """

    def __str__():
        """Returns the URL if possible. Else, it raises a ValueError,
        precising what is missing for the resolution.
        """


class ITraverser(Interface):
    """An interface to traverse using a namespace eg. ++mynamespace++myid
    """

    def traverse(namespace, identifier):
        """Do the traversing of namespace searching for identifier
        """


class IPublisher(Interface):
    """Defines the component in charge of the publication process.
    It usually returns an `IResponse` object.
    """


class IPublicationRoot(Interface):
    """Marker interface for the root of the publication process.
    This marker is usually applied by the publisher or the process
    that start the publication.

    This marker can be used to stop the iteration when calculating
    the lineage of an object in the application tree.
    """


class IPublicationBeginsEvent(Interface):
    """The publication process is about to start.
    """
    root = Attribute('Root used for the publication kickoff.')
    request = Attribute('The request involved in the publication process.')


class IPublicationEndsEvent(Interface):
    """The publication process has ended.
    """
    request = Attribute('The request involved in the publication process.')
    response = Attribute('The response resulting of the publication process.')


@implementer(IPublicationBeginsEvent)
class PublicationBeginsEvent(object):

    def __init__(self, root, request):
        self.root = root
        self.request = request


@implementer(IPublicationEndsEvent)
class PublicationEndsEvent(object):

    def __init__(self, request, response, published_object=None):
        self.request = request
        self.response = response
        self.published_object = published_object


class IHTTPException(Interface):
    code = Attribute("Status code")
    title = Attribute("Status phrase. Eg: 'OK'")


class IHTTPRedirect(IHTTPException):
    location = Attribute("Location of the redirect.")


class Doc(Attribute):
    """Turns the docstring of the given component into an Attribute.
    """
    def __init__(self, component):
        docstring = component.__doc__ or ''
        Attribute.__init__(self, docstring)


class IExchangeMediumsAPI(Interface):
    """Base components defining the input/output.
    """
    IRequest = Doc(IRequest)
    IResponse = Doc(IResponse)


class IPublicationActorsAPI(Interface):
    """The publication actors in charge of transform the input request
    into the output response.
    """
    IWSGIComponent = Doc(IWSGIComponent)
    IPublisher = Doc(IPublisher)
    IPublicationRoot = Doc(IPublicationRoot)
    ITypedRequest = Doc(ITypedRequest)
    ITraverser = Doc(ITraverser)


class IPublicationFlowAPI(Interface):
    """The publication events.
    """
    IPublicationBeginsEvent = Doc(IPublicationBeginsEvent)
    IPublicationEndsEvent = Doc(IPublicationEndsEvent)
    PublicationBeginsEvent = Doc(PublicationBeginsEvent)
    PublicationEndsEvent = Doc(PublicationEndsEvent)


class IComponentsAPI(Interface):
    IRenderable = Doc(IRenderable)
    IView = Doc(IView)
    ILayout = Doc(ILayout)
    IResponseFactory = Doc(IResponseFactory)
    ISlot = Doc(ISlot)
    IViewSlot = Doc(IViewSlot)
    IForm = Doc(IForm)
    ITemplate = Doc(ITemplate)


class ICromlechBrowserAPI(
    IExchangeMediumsAPI,
    IPublicationActorsAPI,
    IPublicationFlowAPI,
    IComponentsAPI):
    IHTTPException = Doc(IHTTPException)
    IHTTPRedirect = Doc(IHTTPRedirect)
    IURL = Doc(IURL)


moduleProvides(ICromlechBrowserAPI)
__all__ = list(ICromlechBrowserAPI)
