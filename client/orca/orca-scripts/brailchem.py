import pyatspi

import orca.script


def is_brailchem_object(object):
    while object:
        if object.name == 'Brailchem':
            return True
        object = object.parent
    return False


class SpeechGenerator(orca.Gecko.SpeechGenerator):

    def _getSpeechForObjectRole(self, obj, role=None):
        if is_brailchem_object(obj) and obj.getRole() == pyatspi.ROLE_PUSH_BUTTON and obj.parent.name == 'Brailchem periodic table window':
            return []
        return orca.Gecko.SpeechGenerator._getSpeechForObjectRole(self, obj, role)

class BrailchemScript(orca.script.Script):

    def getSpeechGenerator(self):
        return SpeechGenerator(self)
