# -*- coding: utf-8 -*-

import pytest
from cromlech import browser
from cromlech.browser import testing
from zope.interface import Interface, verify


def test_request():
    assert verify.verifyClass(
        browser.IHTTPRequest, browser.testing.TestHTTPRequest)

    request = browser.testing.TestHTTPRequest()

    assert verify.verifyObject(browser.IHTTPRequest, request)
    assert request.path == '/'
    assert request.body == ''
    assert request.charset == 'UTF-8'
    assert request.method == 'GET'
    assert request.application_url == 'http://localhost'
    assert request.form == {}

    request = browser.testing.TestHTTPRequest(
        path='/test', method='POST', form={'test': 1})

    assert verify.verifyObject(browser.IHTTPRequest, request)
    assert request.path == '/test'
    assert request.body == ''
    assert request.charset == 'UTF-8'
    assert request.method == 'POST'
    assert request.application_url == 'http://localhost'
    assert request.form == {'test': 1}


def test_response():
    assert verify.verifyClass(
        browser.IHTTPResponse, browser.testing.TestHTTPResponse)

    response = browser.testing.TestHTTPResponse()
    assert verify.verifyObject(browser.IHTTPResponse, response)
    assert response.body == ''
    assert response.headers == {}
    assert response.charset == 'UTF-8'
    assert response.status == '200 - OK'
    assert response.status_int == 200

    response = browser.testing.TestHTTPResponse()
    response.write('something')
    response.write(' and something else')
    assert response.body == 'something and something else'

    response.redirect('somewhere')
    assert response.headers == {'Location': 'somewhere'}
    assert response.status == '302 - Found'
    assert response.status_int == 302

    response.redirect('somewhere', status=305)
    assert response.headers == {'Location': 'somewhere'}
    assert response.status == '305 - Use Proxy'
    assert response.status_int == 305

    response.redirect('somewhere', status=310)
    assert response.headers == {'Location': 'somewhere'}
    assert response.status == '310 - Too many Redirect'
    assert response.status_int == 310

    with pytest.raises(NotImplementedError):
        response.redirect('somewhere', status=404)
        response.redirect('somewhere', status='quack')
        response.redirect('somewhere', status=200)
        response.redirect('somewhere', status=None)


def test_renderer():
    assert verify.verifyClass(
        browser.IRenderer, testing.TestRenderer)

    renderer = testing.TestRenderer()

    assert verify.verifyObject(browser.IRenderer, renderer)
    assert renderer.namespace() == {}
    assert renderer.render() == ''


def test_http_renderer():
    assert browser.IHTTPRenderer.isOrExtends(browser.IRenderer)
    assert verify.verifyClass(
        browser.IHTTPRenderer, testing.TestHTTPRenderer)

    renderer = testing.TestHTTPRenderer()
    assert verify.verifyObject(browser.IHTTPRenderer, renderer)


def test_layout():
    assert browser.ILayout.isOrExtends(browser.IHTTPRenderer)
    assert verify.verifyClass(browser.ILayout, testing.TestLayout)

    layout = testing.TestLayout()
    assert verify.verifyObject(browser.ILayout, layout)


def test_view():
    assert browser.IView.isOrExtends(browser.IHTTPRenderer)
    assert verify.verifyClass(browser.IView, testing.TestView)

    view = testing.TestView()
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
