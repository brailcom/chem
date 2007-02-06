"""This is a text-only test client for the ChemServer"""

import Pyro.core, Pyro.naming
from data_types import Part, Fork


def print_data_structure(data, level=0):
    space = level*"  "
    hit = False
    if "Value" in data.Parentage:
        print space, data, data.value
        hit = True
    if "Fork" in data.Parentage:
        if not hit:
            print space, data
            hit = True
        for l,r in data.links:
            print_data_structure(l, level=level+1)
    if "Complex" in data.Parentage:
        if not hit:
            print space, data
            hit = True
        for l,r in data.parts:
            print_data_structure(l, level=level+1)
    if "Part" in data.Parentage:
        if not hit:
            print space, data
            hit = True
        for l,r in data.neighbors:
            print space, " ", "link to", l



Pyro.core.initClient()
locator = Pyro.naming.NameServerLocator()
ns = locator.getNS()
# ask for an URI
uri = ns.resolve('server')
# connect the server object
server = Pyro.core.getProxyForURI(uri)
# request a session
session = server.connect()
# make the session object process a string
data = session.process_string("") # for fake server it does not matter what we send
# now process the data
print_data_structure(data)
# disconnect the session
server.disconnect(session.number())

