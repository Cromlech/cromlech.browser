# -*- coding: utf-8 -*-

from zope.interface import Interface, Attribute, implements


class IRenderer(Interface):
    """An object meant to render something.
    
    Most of the time, it gets an object and a request and returns
    a response but may also return raw data.
    """

    def update(*args, **kwargs):
        """prepares the rendering
        """

    def render():
        """returns the raw data
        """

    def __call__():
        """
        """


class IView(IRenderer):
    """Grok views all provide this interface"""

    context = Attribute('context', "Object that the view presents.")

    request = Attribute('request', "Request that the view was looked up with.")

    def __call__():
        """
        returns a response object with the body and headers set
        """

class ISecuredItem(Interface):
    """
    """


class ILayout(IRenderer):
    """Global layout view
    """


class IComponent(interface.Interface):
    """A named component
    
    This is intended to be a generic mechanism for composition mechanism
    """
    identifier = interface.Attribute(u"Component id")
    title = interface.Attribute(u"Component title")

    def clone(new_identifier=None):
        """Return a clone of the new component, with identifier
        new_identifier if it is not None.
        """

class ICollection(interface.Interface):
    """Support to manage a collection of ordered named components.
    """
    
    type = interface.Attribute(
        u"Interface restricting the type of component")

    def append(component):
        """Add a new component to the collection. Modify the current
        collection.
        """

    def extend(*component):
        """Create/Add a list of components to the collection. Modify
        the current collection.
        """

    def get(id, default=None):
        """Return the component with the given ID."""

    def select(*ids):
        """Return a copy containing only the given named components."""

    def omit(*ids):
        """Return a copy containing all but none of the given named
        components.
        """

    def copy():
        """Return a copy of the collection."""

    def clear():
        """Empty the collection: remove all components from it."""

    def keys():
        """Return all components id contained in the collection."""

    def __add__(other):
        """Create a collection as copy of self, and add value for
        other component or collection.
        """

    def __getitem__(id):
        """Return the given component identified by id or raise
        KeyError.
        """

    def __contains__(id):
        """Return true if the collection contains a component
        identified by id.
        """

    def __iter__():
        """Return an iterator on the components.
        """

    def __len__():
        """Return the numbre of components.
        """

class IViewlet(IComponent, IRenderer):
    """a viewlet is a component rendering a small part of the global view
    driven by a manager
    """

class IViewletManager(ICollection, IRenderer):
    """compose a set of viewlet together and render in a more global view
    """
