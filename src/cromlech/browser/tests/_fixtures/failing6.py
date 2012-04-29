from cromlech.browser import IRequest, request


class IRequestDerivate(IRequest):
    pass


class YetAnotherItem(object):
    request(IRequest)
    request(IRequestDerivate)
