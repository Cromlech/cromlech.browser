from cromlech.browser import IRequest, request

class ISubRequest(IRequest):
    pass

request(ISubRequest)
