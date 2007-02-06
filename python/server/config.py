import chem_reader_fake

class Config:
    """this is a singleton used to store and share configuration"""

    chem_reader_class = chem_reader_fake.ChemReader
