import twisted.python

import server

class Options(twisted.python.usage.Options):

    optParameters = [
        ['port', 'p', 8000],
        ['user', 'u', 'daemon'],
        ['group', 'g', 'daemon'],
        ]

def makeService(config):
    return server.make_service(config)
