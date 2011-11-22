# -*- coding: utf-8 -*-

from cromlech.browser import IAllowedLanguages
from zope.component import queryUtility
from zope.i18n.config import ALLOWED_LANGUAGES
from zope.i18n.interfaces import INegotiator


def negotiate(context):
    """This method returns a prefered language based on the allowed languages,
    and on the request, passed as 'context'. This could be a good idea to 
    """
    prefs = queryUtility(IAllowedLanguages)
    if prefs is not None:
        allowed = prefs.languages
    else:
        allowed = ALLOWED_LANGUAGES

    if allowed is not None:
        negotiator = queryUtility(INegotiator)
        if negotiator is not None:
            return negotiator.getLanguage(allowed, context)
    return None
