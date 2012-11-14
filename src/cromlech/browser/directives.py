# -*- coding: utf-8 -*-
"""Some directives to link components
"""

import martian
from cromlech.browser.interfaces import IRequest, IView, ISlot
from zope.interface.interfaces import IInterface


def extends_default(directive, value):
    martian.validateInterfaceOrClass(directive, value)
    default = directive.default
    if IInterface.providedBy(value):
        if not value.isOrExtends(default):
            raise martian.error.GrokImportError(
                "%r is not a valid `%s` interface." % (
                    value, default.__name__))
    else:
        if not default.implementedBy(value):
            raise martian.error.GrokImportError(
                "%r must implement the `%s` interface." % (
                    value, default.__name__))


class request(martian.Directive):
    """Restricts a component registration to a request type.
    This request type can be an interface or a class.
    """
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = IRequest
    validate = extends_default


class view(martian.Directive):
    """Links a component to a view.
    This directive is meant to restrict displayable components
    to a given view. This view can be either a class or an interface.
    """
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = IView
    validate = extends_default


class slot(martian.Directive):
    """Links a component to a slot.
    A slot is a hub-like component used to aggregate sub-components.
    """
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = ISlot
    validate = extends_default
