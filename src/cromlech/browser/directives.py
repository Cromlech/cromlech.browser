# -*- coding: utf-8 -*-

import martian
from zope.interface import Interface
from cromlech.browser.interfaces import IManager


def default_view_name(factory, module=None, **data):
    return factory.__name__.lower()


class view(martian.Directive):
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = Interface


class manager(martian.Directive):
    scope = martian.CLASS_OR_MODULE
    store = martian.ONCE
    default = IManager
