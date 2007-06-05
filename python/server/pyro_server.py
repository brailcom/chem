
if __name__ == "__main__":
    # import pyro
    import Pyro.naming, Pyro.core
    #create the server instance
    from chem_server import ChemServer
    server = ChemServer()
    # try if the server works locally
    session = server.connect()
    data = session.process_string("")
    print data
    server.disconnect(session.number())
    # start the pyro machinery
    locator = Pyro.naming.NameServerLocator()
    ns = locator.getNS()
    Pyro.core.initServer()
    daemon = Pyro.core.Daemon()
    daemon.useNameServer(ns)
    # make the server instance available
    daemon.connect(server,'server')
    daemon.requestLoop()
