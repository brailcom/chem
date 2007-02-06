
class DataType:
    """represents a data type"""

    def __init__(self, id, description, long_description=None):
        self._id = id
        self._description = description
        if not long_description:
            self._long_description = self._description
        else:
            self._long_description = long_description

    def id(self):
        return self._id

    def description(self):
        return self._description

    def long_description(self):
        return self._long_description


class DataTypeFactory:
    """singleton used to conveniently create DataType instances"""

    _data_types = {'MW': ('Molecular weight','Molecular weight'),
                   'MF': ('Molecular formula','Molecular formula'),
                   'SUM': ("Summary formula", "Summary formula"),
                   'SMILES': ('SMILES', 'Molecule encoded in SMILES format'),
                   'FRAGMENT': ('Fragment', 'Molecular fragment'),
                   "REACTION": ("Reaction", "Chemical reaction"),
                   "REACTION COMPONENTS": ("Reaction components", "Components of a chemical reaction"),
                   "MOLECULE": ("Molecule","Molecule"),
                   "FRAGMENTS": ("Fragments", "Molecular fragments"),
                   "ATOMS": ("Atoms", "Atoms"),
                   "ATOM": ("Atom", "Atom"),

                   "REL_REACTANT": ("Reactant","Reactant of a reaction"),
                   "REL_PRODUCT": ("Product","Product of a reaction"),
                   "REL_SINGLE_BOND": ("Single bond", "Single bond"),
                   "REL_DOUBLE_BOND": ("Double bond", "Double bond"),
                   "REL_TRIPLE_BOND": ("Triple bond", "Triple bond"),
                   "REL_AROMATIC_BOND": ("Aromatic bond", "Aromatic bond"),
                   "REL_COMPOSED_FROM": ("Composed from", "Composed from"),
                   "REL_REACTS_WITH": ("Reacts with", "Reacts with"),
                   "REL_PRODUCES": ("Produces", "Produces"),
                   "REL_PRODUCED_FROM": ("Produced from", "Produced from"),
                   }

    @classmethod
    def data_type_from_id(self, id):
        """if the data type ID is known, it returns an DataType instance
        filled from a template. Otherwise returns None."""
        if id in self._data_types:
            d, ld = self._data_types[id]
            return DataType(id, d, ld)
        else:
            return None
