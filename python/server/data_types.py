
class DataType:
    """represents a data type"""

    def __init__(self, id, description, long_description=None, default_priority=0):
        self._id = id
        self._description = description
        if not long_description:
            self._long_description = self._description
        else:
            self._long_description = long_description
        self._default_priority = default_priority

    def id(self):
        return self._id

    def description(self):
        return self._description

    def long_description(self):
        return self._long_description

    def default_priority(self):
        return self._default_priority


class DataTypeFactory:
    """singleton used to conveniently create DataType instances"""

    _data_types = {'MW': ('Molecular weight','Molecular weight', 0),
                   'MF': ('Molecular formula','Molecular formula', 15),
                   'SUM': ("Summary formula", "Summary formula", 10),
                   'SMILES': ('SMILES', 'Molecule encoded in SMILES format', 8),
                   'FRAGMENT': ('Fragment', 'Molecular fragment', 0),
                   "REACTION": ("Reaction", "Chemical reaction", 0),
                   "REACTION COMPONENTS": ("Reaction components", "Components of a chemical reaction", 0),
                   "MOLECULE": ("Molecule","Molecule", 0),
                   "FRAGMENTS": ("Fragments", "Molecular fragments", 0),
                   "ATOMS": ("Atoms", "Atoms", 0),
                   "ATOM": ("Atom", "Atom", 0),
                   "NAME": ("Name", "Molecule name", 20),

                   "ATOM_SYMBOL": ("Symbol", "Atom symbol", 20),
                   "EN": ("Electronegativity", "Electronegativity", 0),
                   "ATOM_WEIGHT": ("Atomic weight", "Atomic weight", 0),
                   "VAL_ELECTRONS": ("Valence electrons", "Number of valence electrons", 6),
                   "PROTON_NUMBER": ("Proton number", "Proton number", 10),
                   "OX_NUMBERS": ("Oxidation numbers", "Possible oxidation numbers for an atom", 8),
                   "NAME_LAT": ("Latin name", "Latin name", 0),
                   "NAME_CZ": ("Czech name", "Czech name", 12),
                   "NAME_EN": ("English name", "English name", 15),
                   "DESC": ("Description", "Description", 0),
                   "ORBITALS": ("Electron structure", "Electron structure of occupied orbitals", 0),                   

                   "REL_REACTANT": ("Reactant","Reactant of a reaction", 0),
                   "REL_PRODUCT": ("Product","Product of a reaction", 0),
                   "REL_SINGLE_BOND": ("Single bond", "Single bond", 0),
                   "REL_DOUBLE_BOND": ("Double bond", "Double bond", 0),
                   "REL_TRIPLE_BOND": ("Triple bond", "Triple bond", 0),
                   "REL_AROMATIC_BOND": ("Aromatic bond", "Aromatic bond", 0),
                   "REL_COMPOSED_FROM": ("Composed from", "Composed from", 0),
                   "REL_REACTS_WITH": ("Reacts with", "Reacts with", 0),
                   "REL_PRODUCES": ("Produces", "Produces", 0),
                   "REL_PRODUCED_FROM": ("Produced from", "Produced from", 0),
                   }

    @classmethod
    def data_type_from_id(self, id):
        """if the data type ID is known, it returns an DataType instance
        filled from a template. Otherwise returns None."""
        if id in self._data_types:
            d, ld, def_priority = self._data_types[id]
            return DataType(id, d, long_description=ld, default_priority=def_priority)
        else:
            return None
