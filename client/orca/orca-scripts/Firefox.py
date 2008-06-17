import orca.scripts.toolkits.Gecko

import brailchem

class Script(orca.scripts.toolkits.Gecko.Script):

    def getSpeechGenerator(self):
        return brailchem.SpeechGenerator(self)
