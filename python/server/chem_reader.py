import Pyro.core
from object_types import Value, Part, Complex, MultiView, Relation, PartMultiView, ValuePart, ValuePartMultiView
from data_types import DataTypeFactory, DataType
import oasa
import os, sys
from error_logger import ErrorLogger
from detail_periodic_table import symbol2properties

class ChemReaderException (Exception):

    def __init__(self, text):
        self.text = text

    def __str__(self):
        return "ChemReaderException: " + self.text


class ChemReader:
    """class responsible for reading of chemical data and providing
    an internal representation of them.
    """

    bond_order_to_relation = {1: 'REL_SINGLE_BOND',
                              2: 'REL_DOUBLE_BOND',
                              3: 'REL_TRIPLE_BOND',
                              4: 'REL_AROMATIC_BOND'}

    # reader methods for different formats
    @classmethod
    def _read_smiles(self, text):
        mol = oasa.smiles.text_to_mol(text)
        return mol
    #// reader methods for different formats

    # known formats
    formats = { "SMILES": _read_smiles,
                }


    @classmethod
    def process_string(self, text, format="SMILES"):
        """this is the main method used to process chemical data in a string format to
        the internal representation;
        At present it is only a proxy to process_molecule_string as there is no support
        for reactions yet. After this support is added, it will hopefully be able to
        guess the right kind of data a pass it to the corresponding method."""
        return self.process_molecule_string(text, format=format)

    @classmethod
    def process_molecule_string(self, text, format="SMILES"):
        # check if the format is supported
        if format in self.formats:
            mol = self._read_smiles(text)
        else:
            raise ChemReaderException("unknown format: "+format)
        # shortcut
        id2t = DataTypeFactory.data_type_from_id
        # the molecule
        mol_data = MultiView(id2t("MOLECULE"))
        # add different views
        try:
            name = oasa.name_database.name_molecule(mol, database_file=os.path.join(sys.path[0],"oasa","oasa","names.db"))
        except oasa.oasa_exceptions.oasa_inchi_error, e:
            ErrorLogger.warning("InChI program not properly installed, InChI and name generation won't work. Read README.setup for more info.")
        else:
            if name:
                mol_data.add_view(Value(id2t("NAME"), name['name']))
        mol_data.add_view(Value(id2t("MW"), mol.weight))
        mol_data.add_view(Value(id2t("SUM"), str(mol.get_formula_dict())))
        mol_data_frags = Complex(id2t("FRAGMENTS"))
        mol_data.add_view(mol_data_frags)
        mol_data_atoms = Complex(id2t("ATOMS"))
        mol_data.add_view(mol_data_atoms)
        _atom_to_a_data = {}
        for atom in mol.atoms:
            a_data = ValuePartMultiView(id2t("ATOM"), atom.symbol)
            for key in ('ATOM_SYMBOL','NAME_CZ','VAL_ELECTRONS','DESC','EN','NAME_EN','NAME_LAT','OX_NUMBERS','PROTON_NUMBER','ATOM_WEIGHT'):
                if key in symbol2properties[atom.symbol]:
                    a_data.add_view(Value(id2t(key), symbol2properties[atom.symbol][key]))
            _atom_to_a_data[atom] = a_data
            mol_data_atoms.add_part(Relation(id2t('REL_COMPOSED_FROM'), a_data))
        for atom in mol.atoms:
            a_data = _atom_to_a_data[atom]
            for e,n in atom.get_neighbor_edge_pairs():
                a_data.add_neighbor(Relation(id2t(self.bond_order_to_relation[e.order]), _atom_to_a_data[n]))
        return mol_data
        
