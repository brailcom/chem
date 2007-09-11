import twisted.python

import chem.server

class Options(twisted.python.usage.Options):

    optParameters = [
        ['port', 'p', 8000],
        ['user', 'u', 'daemon'],
        ['group', 'g', 'daemon'],
        ]

def makeService(config):
    return chem.server.twistd.server.make_service(config)
