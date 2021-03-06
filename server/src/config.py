import chem_reader
import os

class Config:
    """this is a singleton used to store and share configuration"""

    # THE CONFIGURATION STARTS HERE
    
    # this can be used to swap between the fake and normal chem_reader
    chem_reader_class = chem_reader.ChemReader
    # this should point to the InChI binary, it overrides the default value in OASA
    oasa_inchi_binary_path = "/usr/local/bin/cInChI-1"
    # where is the translation stored
    translation_dir = os.path.join( os.path.dirname( __file__), "../locale")
    
    # // THE CONFIGURATION ENDS HERE


    # DO NOT MODIFY ANYTHING BELOW UNLESS YOU KNOW WHAT YOU ARE DOING

    @classmethod
    def startup(self):
        import oasa
        oasa.config.Config.inchi_binary_path = self.oasa_inchi_binary_path

