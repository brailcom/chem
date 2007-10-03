
class DataType:
    """represents a data type"""

    def __init__(self, id, description, long_description=None, default_priority=1):
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

    _data_types = {"NAME": ("Name", "Molecule name", 20),
                   'MF': ('Molecular formula','Molecular formula', 15),
                   'SUM': ("Summary formula", "Summary formula", 10),
                   'SMILES': ('SMILES', 'Molecule encoded in SMILES format', 8),
                   'MW': ('Molecular weight','Molecular weight', 5),
                   "FRAGMENTS": ("Fragments", "Molecular fragments", 4),
                   "ATOMS": ("Atoms", "Atoms", 3),

                   "ATOM": ("Atom", "Atom", 1),
                   'FRAGMENT': ('Fragment', 'Molecular fragment', 1),
                   "REACTION": ("Reaction", "Chemical reaction", 1),
                   "REACTION_COMPONENTS": ("Reaction components", "Components of a chemical reaction", 1),
                   "MOLECULE": ("Molecule","Molecule", 1),

                   "ATOM_SYMBOL": ("Symbol", "Atom symbol", 20),
                   "ELEMENT_NAME": ("Element name", "Element name", 19),
                   "PROTON_NUMBER": ("Proton number", "Proton number", 18),
                   "PERIODIC_TABLE_COLUMN": ("Column", "Periodic table column", 17),
                   "PERIODIC_TABLE_ROW": ("Row", "Periodic table row", 16),
                   "ELEMENT_GROUP": ("Element group", "Element group", 15),
                   "VAL_ELECTRONS": ("Valence electrons", "Number of valence electrons", 14),
                   "OX_NUMBERS": ("Oxidation numbers", "Possible oxidation numbers for an atom", 12),
                   "ORBITALS": ("Electron structure", "Electron structure of occupied orbitals", 10),                   
                   "ATOM_WEIGHT": ("Atomic weight", "Atomic weight", 8),
                   "EN": ("Electronegativity", "Electronegativity", 6),
                   "LATIN_ELEMENT_NAME": ("Latin element name", "Latin element name", 4),
                   "DESC": ("Description", "Description", 2),
                   
                   "REL_REACTANT": ("Reactant","Reactant of a reaction", 1),
                   "REL_PRODUCT": ("Product","Product of a reaction", 1),
                   "REL_SINGLE_BOND": ("Single bond", "Single bond", 1),
                   "REL_DOUBLE_BOND": ("Double bond", "Double bond", 1),
                   "REL_TRIPLE_BOND": ("Triple bond", "Triple bond", 1),
                   "REL_AROMATIC_BOND": ("Aromatic bond", "Aromatic bond", 1),
                   "REL_COMPOSED_FROM": ("Composed from", "Composed from", 1),
                   "REL_REACTS_WITH": ("Reacts with", "Reacts with", 1),
                   "REL_PRODUCES": ("Produces", "Produces", 1),
                   "REL_PRODUCED_FROM": ("Produced from", "Produced from", 1),
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
