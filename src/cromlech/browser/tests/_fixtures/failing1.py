from cromlech.browser import request
from zope.interface import Interface


class INotRequest(Interface):
    pass

request(INotRequest)
