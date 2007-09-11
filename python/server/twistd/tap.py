import twisted.python

import server

class Options(twisted.python.usage.Options):

    optParameters = [
        ['port', 'p', 8000],
        ]

def makeService(config):
    return server.make_service(config)
