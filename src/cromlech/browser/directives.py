# -*- coding: utf-8 -*-
"""Some directives to link components
"""

import martian
from cromlech.browser.interfaces import IRequest, IView, IViewSlot
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
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = IRequest
    validate = extends_default


class view(martian.Directive):
    """specify which kind of view an component
    (eg. viewlet or slot) applies to.
    """
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = IView
    validate = extends_default


class slot(martian.Directive):
    """specify which kind of slot a component (eg. viewlet) is part of.
    """
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = IViewSlot
    validate = extends_default
