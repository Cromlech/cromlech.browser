# -*- coding: utf-8 -*-

import pytest
import martian
from cromlech import browser
from cromlech.browser import testing
from cromlech.browser.interfaces import IHTTPException, IView
from zope.interface import verify


def test_request():
    assert verify.verifyClass(
        browser.IRequest, testing.TestRequest)

    request = testing.TestRequest()

    assert verify.verifyObject(browser.IRequest, request)
    assert request.path == '/'
    assert request.body == ''
    assert request.charset == 'UTF-8'
    assert request.method == 'GET'
    assert request.application_url == 'http://localhost'
    assert request.form == {}

    request = testing.TestRequest(
        path='/test', method='POST', form={'test': 1})

    assert verify.verifyObject(browser.IRequest, request)
    assert request.path == '/test'
    assert request.body == ''
    assert request.charset == 'UTF-8'
    assert request.method == 'POST'
    assert request.application_url == 'http://localhost'
    assert request.form == {'test': 1}


def test_response():
    assert verify.verifyClass(
        browser.IResponse, testing.TestResponse)

    response = testing.TestResponse()
    assert verify.verifyObject(browser.IResponse, response)
    assert response.body == ''
    assert response.headers == {}
    assert response.charset == 'UTF-8'
    assert response.status == '200 OK'
    assert response.status_int == 200

    response = testing.TestResponse()
    response.write('something')
    response.write(' and something else')
    assert response.body == 'something and something else'

    response = browser.redirect_response(
        testing.TestResponse, 'somewhere')
    assert response.headers['Location'] == 'somewhere'
    assert response.status == '302 Found'
    assert response.status_int == 302

    response = browser.redirect_response(
        testing.TestResponse, 'somewhere', code=305)
    assert response.headers['Location'] == 'somewhere'
    assert response.status == '305 Use Proxy'
    assert response.status_int == 305

    response = browser.redirect_response(
        testing.TestResponse, 'somewhere', code=310)
    assert response.headers['Location'] == 'somewhere'
    assert response.status == '310 Too many Redirect'
    assert response.status_int == 310

    response = browser.redirect_response(
        testing.TestResponse, 'somewhere', code=307, **{'Dummy': 1})
    assert response.headers['Location'] == 'somewhere'
    assert response.headers['Dummy'] == 1
    assert response.status == '307 Temporary Redirect'
    assert response.status_int == 307

    response = browser.redirect_response(
        testing.TestResponse, 'somewhere', code=302, **{'Location': '/'})
    assert response.headers['Location'] == 'somewhere'
    assert response.status == '302 Found'
    assert response.status_int == 302

    with pytest.raises(RuntimeError):
        browser.redirect_response(
            testing.TestResponse, 'somewhere', code=404)
        browser.redirect_response(
            testing.TestResponse, 'somewhere', code=500)
        browser.redirect_response(
            testing.TestResponse, 'somewhere', code=200)
        browser.redirect_response(
            testing.TestResponse, 'somewhere', code='quack')


def test_redirect_exceptions():
    redirections = browser.exceptions.REDIRECTIONS.items()
    for code, exception in redirections:
        assert code == exception.code
        exc = exception('some location')
        assert exc.location == 'some location'

        response = browser.redirect_exception_response(
            testing.TestResponse, exc)
        assert response.status == "%s %s" % (code, exc.title)
        assert response.headers['Location'] == 'some location'
        assert response.headers['Content-Length'] == '0'
        assert response.headers['Content-Type'] == 'text/plain'


def test_client_error_exceptions():
    client_errors = browser.exceptions.CLIENT_ERRORS.items()
    for code, exception in client_errors:
        try:
            raise exception('test')
        except exception, e:
            assert verify.verifyObject(IHTTPException, e)


def test_layout():
    assert verify.verifyClass(browser.ILayout, testing.TestLayout)

    layout = testing.TestLayout()
    assert verify.verifyObject(browser.ILayout, layout)


def test_html_layout():
    assert verify.verifyClass(browser.ILayout, browser.HTMLWrapper)
    wrapper = browser.HTMLWrapper()
    assert wrapper('<h1>Test !</h1>') == (
        '<html><body><h1>Test !</h1></body></html>')
    assert verify.verifyObject(browser.ILayout, wrapper)


def test_view():
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

    with pytest.raises(martian.error.GrokImportError):

        class WrongValue(object):
            browser.view(object())

    class Dummy(object):
        browser.view(testing.TestView)

    class NoValue(object):
        pass

    assert browser.view.bind().get(Dummy) == testing.TestView
    assert browser.view.bind().get(NoValue) == IView


def test_directive_slot():

    with pytest.raises(martian.error.GrokImportError):

        class WrongValue(object):
            browser.slot(object())

    class Dummy(object):
        browser.slot(testing.TestViewSlot)

    class NoValue(object):
        pass

    assert browser.slot.bind().get(Dummy) == testing.TestViewSlot
    assert browser.slot.bind().get(NoValue) == browser.ISlot


def test_directive_request():

    req = testing.TestRequest()

    class ISomeRequest(browser.IRequest):
        pass

    with pytest.raises(martian.error.GrokImportError):

        class WrongValue(object):
            browser.request(object())

    with pytest.raises(martian.error.GrokImportError):

        class InstanceValue(object):
            browser.request(req)

    class Basic(object):
        browser.request(ISomeRequest)

    class NoValue(object):
        pass

    assert browser.request.bind().get(Basic) == ISomeRequest
    assert browser.request.bind().get(NoValue) == browser.IRequest
