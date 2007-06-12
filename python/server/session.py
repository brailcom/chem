from config import Config

class Session:
    """represents one session""" 

    def __init__(self, session_number):
        self._number = session_number
        self._data = None

    def number(self):
        return self._number

    def process_string(self, data):
        Config.startup()
        self._data = Config.chem_reader_class.process_string(data) 
        return self.data()

    def data(self):
        return self._data
