# -*- coding: utf-8 -*-

import threading


class SessionInfo(threading.local):
    """Session hook land.
    """
    session = None


sessioninfo = SessionInfo()


def setSession(session=None):
    sessioninfo.session = session


def getSession():
    return sessioninfo.session
