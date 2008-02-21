from object_types import Value, Part, Complex, MultiView, Relation, PartMultiView, ValuePart, LanguageDependentValue
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

    # known formats
    formats = { "SMILES": "_read_smiles",
                "Molfile": "_read_molfile",
                "summary": "_read_summary_formula",
                }

    table_key_to_data_type = {'ATOM_SYMBOL':'ATOM_SYMBOL',
                              'VAL_ELECTRONS':'VAL_ELECTRONS',
                              'EN':'EN',
                              'NAME_LAT':'LATIN_ELEMENT_NAME',
                              'OX_NUMBERS':'OX_NUMBERS',
                              'PROTON_NUMBER':'PROTON_NUMBER',
                              'ATOM_WEIGHT':'ATOM_WEIGHT',
                              'ORBITALS':'ORBITALS',
                              'ROW':'PERIODIC_TABLE_ROW',
                              'COLUMN':'PERIODIC_TABLE_COLUMN',
                              'group':'ELEMENT_GROUP',
                              'NAMES':'ELEMENT_NAME',
                              }

    @classmethod
    def known_formats(self):
        """returns a list of all currently supported formats."""
        return self.formats.keys()

    @classmethod
    def process_string(self, text, format="SMILES"):
        """this is the main method used to process chemical data in a string format to
        the internal representation;"""
        # check if the format is supported
        if format in self.formats:
            chem_objects = getattr(self,self.formats[format])(text)
        else:
            raise ChemReaderException("unknown format: "+format)
        # shortcut
        id2t = DataTypeFactory.data_type_from_id
        result = Complex(id2t("RESULT"))
        for chem_object in chem_objects:
            if chem_object.__class__.__name__ == "molecule":
                chem_data = self.process_molecule(chem_object)
            elif chem_object.__class__.__name__ == "reaction":
                chem_data = self.process_reaction(chem_object)
            else:
                raise ChemReaderException("unsupported chem_object class: "+chem_object.__class__.__name__)
            result.add_part(Relation(id2t('REL_COMPOSED_FROM'), chem_data))
        return result

    @classmethod
    def process_molecule(self, mol):
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
                mol_data.add_view(LanguageDependentValue(id2t("NAME"), {'en':name['name']}))
        mol_data.add_view(Value(id2t("MW"), mol.weight))
        mol_data.add_view(Value(id2t("SUM"), str(mol.get_formula_dict())))
        mol_data_frags = Complex(id2t("FRAGMENTS"))
        mol_data.add_view(mol_data_frags)
        mol_data_atoms = Complex(id2t("ATOMS"))
        mol_data.add_view(mol_data_atoms)
        _atom_to_a_data = {} # maps oasa atoms to brailchem data
        for atom in mol.atoms:
            a_data = PartMultiView(id2t("ATOM"))
            # element names in diffent languages
            a_data.add_view(LanguageDependentValue(id2t("ELEMENT_NAME"), symbol2properties[atom.symbol]['NAMES']))
            # description is also langugage dependent
            if symbol2properties[atom.symbol]['DESC']:
                a_data.add_view(LanguageDependentValue(id2t("DESC"), symbol2properties[atom.symbol]['DESC']))
            # other atom data
            for key,dtype in self.table_key_to_data_type.iteritems():
                if key in symbol2properties[atom.symbol] and key != 'NAMES':
                    value = symbol2properties[atom.symbol][key]
                    if type(value) == type([]):
                        value = ",".join(map(str, value))
                    else:
                        a_data.add_view(Value(id2t(dtype), value))
            _atom_to_a_data[atom] = a_data
            mol_data_atoms.add_part(Relation(id2t('REL_COMPOSED_FROM'), a_data))
        for atom in mol.atoms:
            a_data = _atom_to_a_data[atom]
            for e,n in atom.get_neighbor_edge_pairs():
                a_data.add_neighbor(Relation(id2t(self.bond_order_to_relation[e.order]), _atom_to_a_data[n]))
        # fragment support - just for testing
        for (smiles_text,name,compound_type) in [("C(=O)H","carbonyl group","aldehyde"),
                                                 ("C(=O)OH","carboxyl group","carboxylic acid")]:
            fragment_mol = oasa.smiles.text_to_mol(smiles_text)
            for fragment in mol.select_matching_substructures(fragment_mol, implicit_freesites=True):
                frag_data = PartMultiView(id2t("FRAGMENT"))
                frag_data.add_view(LanguageDependentValue(id2t("FRAGMENT_NAME"), {"en":name}))
                frag_data.add_view(LanguageDependentValue(id2t("FRAGMENT_COMPOUND_TYPE"), {"en":compound_type}))
                frag_data_atoms = Complex(id2t("ATOMS"))
                frag_data.add_view(frag_data_atoms)
                for atom in fragment:
                    frag_data_atoms.add_part(Relation(id2t('REL_COMPOSED_FROM'), _atom_to_a_data[atom]))
                mol_data_frags.add_part(Relation(id2t('REL_COMPOSED_FROM'), frag_data))

        # // fragment support
        return mol_data

    @classmethod
    def process_reaction(self, react):
        def add_reaction_components_to_reaction(data_type, comps):
            if len(comps) > 0:
                top = Complex(id2t(data_type))
                r_component_data.add_part(Relation(id2t("REL_COMPOSED_FROM"), top))
                for comp in comps:
                    mol_data = self.process_molecule(comp.molecule)
                    top.add_part(Relation(id2t("REL_COMPOSED_FROM"), mol_data))
        # shortcut
        id2t = DataTypeFactory.data_type_from_id
        # the molecule
        r_data = MultiView(id2t("REACTION"))
        r_component_data = Complex(id2t("REACTION_COMPONENTS"))
        r_data.add_view(r_component_data)
        add_reaction_components_to_reaction( "REACTANTS", react.reactants)
        add_reaction_components_to_reaction( "REAGENTS", react.reagents)
        add_reaction_components_to_reaction( "PRODUCTS", react.products)
        return r_data

    ## ---------- private methods ----------
        
    # reader methods for different formats
    @classmethod
    def _read_smiles(self, text):
        converter = oasa.smiles.converter()
        return converter.read_text(text)

    @classmethod
    def _read_molfile(self, text):
        mol = oasa.molfile.text_to_mol(text)
        return [mol]

    @classmethod
    def _read_summary_formula(self, text):
        sum_dict = oasa.periodic_table.formula_dict(text)
        mol = oasa.molecule()
        for (symbol,count) in sum_dict.iteritems():
            for i in range(count):
                a = oasa.atom(symbol)
                a.valency = 0
                mol.add_vertex(a)
        return [mol]
    #// reader methods for different formats

    #// ---------- private methods ----------
