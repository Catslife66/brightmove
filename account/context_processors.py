from .visitor import Visitor

def visitor(request):
    return {'visitor': Visitor(request)}