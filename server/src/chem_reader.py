from object_types import Value, Part, Complex, MultiView, Relation, PartMultiView, ValuePart, LanguageDependentValue
from data_types import DataTypeFactory, DataType
import oasa
import os, sys
from error_logger import ErrorLogger
from detail_periodic_table import symbol2properties
import i18n
_ = i18n.TranslatableTextFactory("brailchem")


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

    stereochemistry_to_relation = {
        oasa.stereochemistry.cis_trans_stereochemistry.OPPOSITE_SIDE: "REL_OPPOSITE_SIDE",
        oasa.stereochemistry.cis_trans_stereochemistry.SAME_SIDE: "REL_SAME_SIDE",
        }

    # known formats
    formats = { "SMILES": ("_read_smiles", _("SMILES"), ()),
                "Molfile": ("_read_molfile", _("Molfile"), ('mol',)),
                "summary": ("_read_summary_formula", _("Summary formula"), ()),
                "name": ("_read_name", _("Name"), ()),
                }

    # the following is a list of most important supported formats (when openbabel is available)
    # this is mainly here for the client to be able to suggest most common formats
    important_formats = ["SMILES","name","cdx","cdxml","cml","inchi","pdb","sdf"]

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
    def known_format_names(self):
        """returns a list of tuples of currently supported formats and their descriptions."""
        keys = self.formats.keys()
        keys.sort()
        return [(key,self.formats[key][1]) for key in keys]

    @classmethod
    def known_format_descriptions(self):
        """returns a list of tuples of currently supported formats and their descriptions."""
        keys = self.formats.keys()
        keys.sort()
        return [(key,self.formats[key][1],self.formats[key][2]) for key in keys]

    @classmethod
    def process_string(self, text, format="SMILES"):
        """this is the main method used to process chemical data in a string format to
        the internal representation;"""
        # check if the format is supported
        if format in self.formats:
            method,name,_ext = self.formats[format]
            if callable(method):
                chem_objects = method(text)
            else:
                chem_objects = getattr(self,method)(text)
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
            names = oasa.structure_database.find_molecule_in_database(mol, database_file=os.path.join(sys.path[0],"oasa","oasa","structures.db"))
        except oasa.oasa_exceptions.oasa_inchi_error, e:
            ErrorLogger.warning("InChI program not properly installed, InChI and name generation won't work. Read README.setup for more info.")
        else:
            if names:
                mol_data.add_view(LanguageDependentValue(id2t("NAME"), {'en':names[0][1]}))
        mol_data.add_view(Value(id2t("MW"), mol.weight))
        mol_data.add_view(Value(id2t("SUM"), str(mol.get_formula_dict())))
        mol_data.add_view(Value(id2t("MOL_CHARGE"), mol.charge))
        mol_data.add_view(Value(id2t("MOL_MULTIPLICITY"), 1+sum([v.multiplicity-1 for v in mol.vertices])))
        mol_data_frags = Complex(id2t("FRAGMENTS"))
        mol_data.add_view(mol_data_frags)
        mol_data_atoms = Complex(id2t("ATOMS"))
        mol_data.add_view(mol_data_atoms)
        _atom_to_a_data = {} # maps oasa atoms to brailchem data
        # _rings are used for statistical information on an atom
        _rings = mol.get_smallest_independent_cycles()
        for atom in mol.atoms:
            a_data = PartMultiView(id2t("ATOM"))
            # charge and multiplicity
            a_data.add_view(Value(id2t("ATOM_CHARGE"), atom.charge))
            a_data.add_view(Value(id2t("ATOM_MULTIPLICITY"), atom.multiplicity))
            # element names in diffent languages
            a_data.add_view(LanguageDependentValue(id2t("ELEMENT_NAME"), symbol2properties[atom.symbol]['NAMES']))
            # description is also langugage dependent
            if symbol2properties[atom.symbol]['DESC']:
                a_data.add_view(LanguageDependentValue(id2t("DESC"), symbol2properties[atom.symbol]['DESC']))
            # group also
            if symbol2properties[atom.symbol]['group']:
                a_data.add_view(LanguageDependentValue(id2t("ELEMENT_GROUP"), symbol2properties[atom.symbol]['group']))
            # other atom data
            for key,dtype in self.table_key_to_data_type.iteritems():
                if key in symbol2properties[atom.symbol] and key not in ('NAMES','group'):
                    value = symbol2properties[atom.symbol][key]
                    if type(value) == type([]):
                        value = ",".join(map(str, value))
                    else:
                        a_data.add_view(Value(id2t(dtype), value))
            # statistical topological data
            _num_rings = len([rng for rng in _rings if atom in rng])
            a_data.add_view(Value(id2t("PART_OF_RINGS"), _num_rings))
            _atom_to_a_data[atom] = a_data
            mol_data_atoms.add_part(Relation(id2t('REL_COMPOSED_FROM'), a_data))
        # before processing bonds, we must detect aromatic bonds
        mol.mark_aromatic_bonds()
        for atom in mol.atoms:
            a_data = _atom_to_a_data[atom]
            for e,n in atom.get_neighbor_edge_pairs():
                rel = Relation(id2t(self.bond_order_to_relation[e.order]), _atom_to_a_data[n])
                rel.set_property("aromatic",e.aromatic)
                a_data.add_neighbor(rel)
        # stereochemistry support
        for stereo in mol.stereochemistry:
            if stereo.__class__.__name__ == "cis_trans_stereochemistry":
                atom1 = stereo.references[0]
                atom2 = stereo.references[-1]
                a_data1 = _atom_to_a_data[atom1]
                a_data2 = _atom_to_a_data[atom2]
                relation_name = self.stereochemistry_to_relation[stereo.value]
                a_data1.add_neighbor(Relation(id2t(relation_name), a_data2))
                a_data2.add_neighbor(Relation(id2t(relation_name), a_data1))                                     
        # fragment support
        ssm = oasa.subsearch.substructure_search_manager()
        hits = ssm.find_substructures_in_mol(mol)
        rings = [h for h in hits if isinstance(h, oasa.subsearch.ring_match)]
        _hit_to_data = {}
        for hit in hits:
            frag_data = PartMultiView(id2t("FRAGMENT"))
            _hit_to_data[hit] = frag_data
            frag_data.add_view(LanguageDependentValue(id2t("FRAGMENT_NAME"), {"en":hit.substructure.name}))
            frag_data.add_view(LanguageDependentValue(id2t("FRAGMENT_COMPOUND_TYPE"), {"en":hit.substructure.compound_type}))
            frag_data_atoms = Complex(id2t("ATOMS"))
            frag_data.add_view(frag_data_atoms)
            for atom in hit.get_significant_atoms():
                frag_data_atoms.add_part(Relation(id2t('REL_COMPOSED_FROM'), _atom_to_a_data[atom]))
            mol_data_frags.add_part(Relation(id2t('REL_COMPOSED_FROM'), frag_data))
        # add relations between rings
        for i,ring1 in enumerate(rings):
            for ring2 in rings[i+1:]:
                common_atoms = set( ring1.get_significant_atoms()) & set( ring2.get_significant_atoms())
                if common_atoms:
                    d1 = _hit_to_data[ring1]
                    d2 = _hit_to_data[ring2]
                    count = len(common_atoms)
                    data_type = DataType("SHARED_ATOMS",
                                         _("%d shared atoms")%count,
                                         _("The ring shares %d atoms with the neighbor ring"%count))
                    d1.add_neighbor(Relation(data_type, d2))
                    d2.add_neighbor(Relation(data_type, d1))
        # // fragment support
        # svg picture support
        for (atom,data) in _atom_to_a_data.iteritems():
            atom.properties_['svg_id'] = str(data.id())
        svg_xml = self._generate_svg(mol)
        mol_data.add_view(Value(id2t("MOL_PICTURE"), svg_xml))
        # // svg picture support
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

    @classmethod
    def _generate_svg(self, mol):
        def add_circles( self):
          for v in self.molecule.vertices:
            if 'svg_id' in v.properties_:
              id = "h-" + v.properties_['svg_id']
            else:
              id = ""
            self._draw_circle( self.top,
                               self.transformer.transform_xy(v.x,v.y),
                               radius=8,
                               fill_color="#f00",
                               stroke_color="#000",
                               id=id)
        from oasa import svg_out
        svg_out = svg_out.svg_out()
        mol.normalize_bond_length( 30)
        svg = svg_out.mol_to_svg(mol, after=add_circles)
        return svg.toxml()

        
    # reader methods for different formats
    @classmethod
    def _read_smiles(self, text):
        converter = oasa.smiles.converter()
        mols = []
        for line in text.splitlines():
            mols += converter.read_text(line)
        return mols

    @classmethod
    def _read_molfile(self, text):
        mol = oasa.molfile.text_to_mol(text)
        mol.detect_stereochemistry_from_coords()
        return [mol]

    @classmethod
    def _read_summary_formula(self, text):
        mols = []
        for line in text.splitlines():
            sum_dict = oasa.periodic_table.formula_dict(line)
            mol = oasa.molecule()
            for (symbol,count) in sum_dict.iteritems():
                for i in range(count):
                    a = oasa.atom(symbol)
                    a.valency = 0
                    mol.add_vertex(a)
            mols.append(mol)
        return mols

    @classmethod
    def _read_name(self, text):
        def _key(hit):
            return len(hit[3])
        mols = []
        for line in text.splitlines():
            res = oasa.structure_database.get_compounds_from_database(name=line)
            res += oasa.structure_database.get_compounds_from_database(synonym=line) 
            # find the hit with shortest smiles - this should be appropriate in most cases
            res.sort(key=_key)
            if res:
                converter = oasa.smiles.converter()
                mols += converter.read_text(res[0][3])
        return mols

    @classmethod
    def _read_pybel_text(self, format, text):
        conv = oasa.pybel_bridge.PybelConverter
        mols = conv.read_text(format, text)
        for mol in mols:
            if len([1 for a in mol.vertices if a.x==0 and a.y==0]) == len(mol.vertices):
                # coordinates are not present (everything is zero)
                for a in mol.vertices:
                    a.x, a.y, a.z = None, None, None
                cg = oasa.coords_generator.coords_generator()
                cg.calculate_coords(mol)
            else:
                mol.detect_stereochemistry_from_coords()
        return mols

    #// reader methods for different formats

    #// ---------- private methods ----------


# some setup

if hasattr(oasa, 'pybel_bridge'):
    import pybel
    def create_read_func( format):
        return lambda text: ChemReader._read_pybel_text(format, text)
    for format,name in pybel.informats.iteritems():
        if format == "sdf":
            # add mol and mdl to sdf - these are the same
            ChemReader.formats[format] = (create_read_func(format), name, (format,"mol","mdl"))
        else:
            ChemReader.formats[format] = (create_read_func(format), name, (format,))
