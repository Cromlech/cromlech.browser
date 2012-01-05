# -*- coding: utf-8 -*-

import pytest
from cromlech import browser
from cromlech.browser import testing
from zope.interface import Interface, verify


def test_request():
    assert verify.verifyClass(
        browser.IHTTPRequest, testing.TestHTTPRequest)

    request = testing.TestHTTPRequest()

    assert verify.verifyObject(browser.IHTTPRequest, request)
    assert request.path == '/'
    assert request.body == ''
    assert request.charset == 'UTF-8'
    assert request.method == 'GET'
    assert request.application_url == 'http://localhost'
    assert request.form == {}

    request = testing.TestHTTPRequest(
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
        browser.IHTTPResponse, testing.TestHTTPResponse)

    response = testing.TestHTTPResponse()
    assert verify.verifyObject(browser.IHTTPResponse, response)
    assert response.body == ''
    assert response.headers == {}
    assert response.charset == 'UTF-8'
    assert response.status == '200 OK'
    assert response.status_int == 200

    response = testing.TestHTTPResponse()
    response.write('something')
    response.write(' and something else')
    assert response.body == 'something and something else'

    response = browser.redirect_response(
        testing.TestHTTPResponse, 'somewhere')
    assert response.headers == {'Location': 'somewhere'}
    assert response.status == '302 Found'
    assert response.status_int == 302

    response = browser.redirect_response(
        testing.TestHTTPResponse, 'somewhere', code=305)
    assert response.headers == {'Location': 'somewhere'}
    assert response.status == '305 Use Proxy'
    assert response.status_int == 305

    response = browser.redirect_response(
        testing.TestHTTPResponse, 'somewhere', code=310)
    assert response.headers == {'Location': 'somewhere'}
    assert response.status == '310 Too many Redirect'
    assert response.status_int == 310

    response = browser.redirect_response(
        testing.TestHTTPResponse, 'somewhere', code=307, **{'Dummy': 1})
    assert response.headers == {'Dummy': 1, 'Location': 'somewhere'}
    assert response.status == '307 Temporary Redirect'
    assert response.status_int == 307

    response = browser.redirect_response(
        testing.TestHTTPResponse, 'somewhere', code=302, **{'Location': '/'})
    assert response.headers == {'Location': 'somewhere'}
    assert response.status == '302 Found'
    assert response.status_int == 302

    with pytest.raises(RuntimeError):
        browser.redirect_response(
            testing.TestHTTPResponse, 'somewhere', code=404)
        browser.redirect_response(
            testing.TestHTTPResponse, 'somewhere', code=500)
        browser.redirect_response(
            testing.TestHTTPResponse, 'somewhere', code=200)
        browser.redirect_response(
            testing.TestHTTPResponse, 'somewhere', code='quack')


def test_exceptions():
    redirections = browser.exceptions.REDIRECTIONS.items()
    for code, exception in redirections:
        assert code == exception.code
        exc = exception('some location')
        assert exc.location == 'some location'

        response = browser.redirect_exception_response(
            testing.TestHTTPResponse, exc)
        assert response.status == "%s %s" % (code, exc.title)


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
