# -*- coding: utf-8 -*-
"""
Some directives to link components
"""

import martian
from zope.interface import Interface
from cromlech.browser.interfaces import IManager


def default_view_name(factory, module=None, **data):
    """A view is, by default registered under its lowercase name."""
    return factory.__name__.lower()


class view(martian.Directive):
    """specify which kind of view an component
    (eg. viewlet or slot) applies to"""
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = Interface


class slot(martian.Directive):
    """specify which kind of slot a component (eg. viewlet) is part of"""
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = IManager
