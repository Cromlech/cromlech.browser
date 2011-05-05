# -*- coding: utf-8 -*-

import pytest
import martian
import martian.testing
from cromlech import browser
from zope.interface import Interface, verify


def test_renderer():
    assert verify.verifyClass(
        browser.IRenderer, browser.testing.TestRenderer)

    renderer = browser.testing.TestRenderer()

    assert verify.verifyObject(browser.IRenderer, renderer)
    assert renderer.namespace() == {}
    assert renderer.render() == ''


def test_http_renderer():
    assert browser.IHTTPRenderer.isOrExtends(browser.IRenderer)
    assert verify.verifyClass(
        browser.IHTTPRenderer, browser.testing.TestHTTPRenderer)

    renderer = browser.testing.TestHTTPRenderer()
    assert verify.verifyObject(browser.IHTTPRenderer, renderer)


def test_layout():
    assert browser.ILayout.isOrExtends(browser.IHTTPRenderer)
    assert verify.verifyClass(browser.ILayout, browser.testing.TestLayout)

    layout = browser.testing.TestLayout()
    assert verify.verifyObject(browser.ILayout, layout)


def test_view():
    assert browser.IView.isOrExtends(browser.IHTTPRenderer)
    assert verify.verifyClass(browser.IView, browser.testing.TestView)

    view = browser.testing.TestView()
    assert verify.verifyObject(browser.IView, view)


def test_session():
    session_object = object()
    browser.setSession(session_object)

    assert browser.session.sessioninfo.__class__ == (
        browser.session.SessionInfo)

    assert browser.session.sessioninfo.session is session_object
    assert browser.session.sessioninfo.session is browser.getSession()

    browser.setSession()
    assert browser.session.sessioninfo.session is None
    assert browser.session.sessioninfo.session is None


def test_directive_view():

    view = object()

    class Dummy(object):
        browser.view(view)

    class NoValue(object):
        pass

    assert browser.view.bind().get(Dummy) == view
    assert browser.view.bind().get(NoValue) == Interface

    assert browser.default_view_name(Dummy) == 'dummy'
    assert browser.default_view_name(NoValue) == 'novalue'


def test_directive_slot():

    slot = object()

    class Dummy(object):
        browser.slot(slot)

    class NoValue(object):
        pass

    assert browser.slot.bind().get(Dummy) == slot
    assert browser.slot.bind().get(NoValue) == browser.IViewSlot
