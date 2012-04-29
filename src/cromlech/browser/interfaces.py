# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute, implements, moduleProvides


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


class IResponse(Interface):
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


class IRenderer(Interface):
    """An object meant to render something.

    Most of the time, it gets an object and a request and returns
    a response but may also return raw data.
    """

    def update(**kwargs):
        """Prepares the rendering.
        """

    def render(**kwargs):
        """Returns the raw data.
        """


class ILayout(IRenderer):
    """A layout serves as a content decoration. Mainly used to maintain
    a site identity, it can be used as a simple renderer. Its `render`
    method uses the `content` argument as the content to be wrapped.
    """
    def render(content, **layout_environ):
        """Wraps the content into a 'decoration'. The `layout_environ`
        dict can contain additional data helping to render this component.
        """


class IView(IRenderer):
    """A renderer returning an HTTPResponse
    """
    def __call__(**kwargs):
        """Returns a response object with the body and headers set.
        """


class IViewSlot(IRenderer):
    """A fragment of a view, acting as an aggregator of sub-renderers.
    """
    view = Attribute("Renderer on which the slot is called.")


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
    def render(component, target_language=None, **namespace):
        """Renders the given component.
        """


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


class IWSGIResponsive(Interface):
    """Defines a component that is able to respond to a direct WSGI Call.
    More widely, this defines the very basics of a WSGI Application.
    """
    def __call__(environ, start_response):
        """Cooks a valid WSGI response thanks to start_response,
        setting headers and returning an iterable body.
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


class PublicationBeginsEvent(object):
    implements(IPublicationBeginsEvent)

    def __init__(self, root, request):
        self.root = root
        self.request = request


class PublicationEndsEvent(object):
    implements(IPublicationEndsEvent)

    def __init__(self, request, response, published_object=None):
        self.request = request
        self.response = response
        self.published_object = published_object


class IHTTPException(Interface):
    code = Attribute("Status code")
    title = Attribute("Status phrase. Eg: 'OK'")


class IHTTPRedirect(IHTTPException):
    location = Attribute("Location of the redirect.")


class IExchangeMediumsAPI(Interface):
    """Base components defining the input/output.
    """
    IRequest = Attribute("The input component.")
    IResponse = Attribute("The output component.")


class IPublicationActorsAPI(Interface):
    """The publication actors in charge of transform the input request
    into the output response.
    """
    IWSGIResponsive = Attribute("The WSGI application.")
    IPublisher = Attribute("The component in charge of the publication.")
    IPublicationRoot = Attribute("The root of the requested resouce.")
    ITypedRequest = Attribute("Base interface for request marker interfaces")


class IPublicationFlowAPI(Interface):
    """The publication events.
    """
    IPublicationBeginsEvent = Attribute("A publication is about to start.")
    IPublicationEndsEvent = Attribute("A publication has ended.")
    PublicationBeginsEvent = Attribute("")
    PublicationEndsEvent = Attribute("")


class IComponentsAPI(Interface):
    IRenderer = Attribute("")
    ILayout = Attribute("")
    IView = Attribute("")
    IViewSlot = Attribute("")
    IForm = Attribute("")
    ITemplate = Attribute("")  


class ICromlechBrowserAPI(
    IExchangeMediumsAPI,
    IPublicationActorsAPI,
    IPublicationFlowAPI,
    IComponentsAPI):
    IHTTPException = Attribute("")
    IHTTPRedirect = Attribute("")
    IURLResolver = Attribute("")
    

moduleProvides(ICromlechBrowserAPI)
__all__ = list(ICromlechBrowserAPI)
