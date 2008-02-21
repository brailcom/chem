import i18n
_ = i18n.TranslatableTextFactory("brailchem")

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

    _data_types = {"RESULT": (_("Result"), _("Result"), 1),  # result is the uppermost node in the hierarchy

                   "NAME": (_("Name"), _("Compound name"), 20),
                   'MF': (_('Molecular formula'),_('Molecular formula'), 15),
                   'SUM': (_("Summary formula"), _("Summary formula"), 10),
                   'SMILES': (_('SMILES'), _('Molecule encoded in SMILES format'), 8),
                   'MW': (_('Molecular weight'), _('Molecular weight'), 5),
                   "FRAGMENTS": (_("Fragments"), _("Molecular fragments"), 4),
                   "ATOMS": (_("Atoms"), _("Atoms"), 3),

                   "ATOM": (_("Atom"), _("Atom"), 1),
                   'FRAGMENT': (_('Fragment'), _('Molecular fragment'), 1),
                   "REACTION": (_("Reaction"), _("Chemical reaction"), 1),
                   "REACTANTS": (_("Reactants"), _("Starting compounds of a reaction"), 1),
                   "REAGENTS": (_("Reagents"), _("Additional components of a reaction - solvent, catalyst, etc."), 1),
                   "PRODUCTS": (_("Products"), _("Products of a chemical reaction"), 1),
                   "REACTION_COMPONENTS": (_("Reaction components"), _("Components of a chemical reaction"), 1),
                   "MOLECULE": (_("Molecule"), _("Molecule"), 1),

                   'FRAGMENT_NAME': (_('Fragment name'), _('Name of the chemical group this fragment represents'), 20),
                   'FRAGMENT_COMPOUND_TYPE': (_('Compound type'), _('Type of compound this fragment represents'), 15),

                   "ATOM_SYMBOL": (_("Symbol"), _("Atom symbol"), 20),
                   "ELEMENT_NAME": (_("Element name"), _("Element name"), 19),
                   "PROTON_NUMBER": (_("Proton number"), _("Proton number"), 18),
                   "PERIODIC_TABLE_COLUMN": (_("Column"), _("Periodic table column"), 17),
                   "PERIODIC_TABLE_ROW": (_("Row"), _("Periodic table row"), 16),
                   "ELEMENT_GROUP": (_("Element group"), _("Element group"), 15),
                   "VAL_ELECTRONS": (_("Valence electrons"), _("Number of valence electrons"), 14),
                   "OX_NUMBERS": (_("Oxidation numbers"), _("Possible oxidation numbers for an atom"), 12),
                   "ORBITALS": (_("Electron structure"), _("Electron structure of occupied orbitals"), 10),                   
                   "ATOM_WEIGHT": (_("Atomic weight"), _("Atomic weight"), 8),
                   "EN": (_("Electronegativity"), _("Electronegativity"), 6),
                   "LATIN_ELEMENT_NAME": (_("Latin element name"), _("Latin element name"), 4),
                   "DESC": (_("Description"), _("Description"), 2),
                   
                   "REL_REACTANT": (_("Reactant"), _("Reactant of a reaction"), 1),
                   "REL_PRODUCT": (_("Product"), _("Product of a reaction"), 1),
                   "REL_SINGLE_BOND": (_("Single bond"), _("Single bond"), 1),
                   "REL_DOUBLE_BOND": (_("Double bond"), _("Double bond"), 1),
                   "REL_TRIPLE_BOND": (_("Triple bond"), _("Triple bond"), 1),
                   "REL_AROMATIC_BOND": (_("Aromatic bond"), _("Aromatic bond"), 1),
                   "REL_COMPOSED_FROM": (_("Composed from"), _("Composed from"), 1),
                   "REL_REACTS_WITH": (_("Reacts with"), _("Reacts with"), 1),
                   "REL_PRODUCES": (_("Produces"), _("Produces"), 1),
                   "REL_PRODUCED_FROM": (_("Produced from"), _("Produced from"), 1),
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

