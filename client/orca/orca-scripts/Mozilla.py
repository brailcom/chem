import orca.scripts.Mozilla

import brailchem

class Script(orca.scripts.Mozilla.Script):

    def getSpeechGenerator(self):
        return brailchem.SpeechGenerator(self)
