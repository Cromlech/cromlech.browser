from cromlech.browser import IRequest, request


class IAnotherSubRequest(IRequest):
    pass


request(IRequest)
request(IAnotherSubRequest)
