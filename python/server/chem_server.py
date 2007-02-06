import Pyro.core
from session import Session

class ChemServer(Pyro.core.ObjBase):
    """chem server is the only object that is made available through Pyro.
    It manages sessions (session.Session) that do the actual work"""

    def __init__(self):
        Pyro.core.ObjBase.__init__(self)
        self._sessions = {}

    def connect(self, session_id=None):
        """if the session_id is not given, a new session is to be created,
        otherwise return an existing session.
        """
        if session_id == None or not session_id in self._sessions:
            i = 1
            while i in self._sessions.keys():
                i += 1
            ses = Session(i)
            self._sessions[i] = ses
        else:
            ses = self._sessions[session_id]
        print self._sessions
        return ses

    def disconnect(self, session_id):
        """removes the session from active sessions"""
        if not session_id in self._sessions:
            raise ValueError("session with this number does not exist")
        else:
            del self._sessions[session_id]
        print self._sessions
