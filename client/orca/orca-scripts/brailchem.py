import pyatspi

import orca.scripts.toolkits.Gecko


def is_brailchem_object(object):
    while object:
        if object.name == 'Brailchem':
            return True
        object = object.parent
    return False


class SpeechGenerator(orca.scripts.toolkits.Gecko.SpeechGenerator):

    def _getSpeechForObjectRole(self, obj, role=None):
        if (is_brailchem_object(obj) and obj.getRole() == pyatspi.ROLE_PUSH_BUTTON and
            (obj.parent.name == 'chrome://brailchem/content/periodic.xul' or
             obj.parent.parent.name == 'chrome://brailchem/content/periodic.xul')):
            return []
        return orca.scripts.toolkits.Gecko.SpeechGenerator._getSpeechForObjectRole(self, obj, role)

class BrailchemScript(orca.script.Script):

    def getSpeechGenerator(self):
        return SpeechGenerator(self)
