# -*- coding: utf-8 -*-

from cromlech.browser.exceptions import REDIRECTION


def redirect_response(responseFactory, url, code=302, **additional_headers):
    """Creates a redirect response.
    """
    if not code in REDIRECTION:
        raise NotImplementedError('This is not a redirection')

    headers = {}
    if additional_headers:
        headers.update(additional_headers)
    headers['Location'] = url

    status = REDIRECTION[status]
    return responseFactory(status=status, headers=headers)
