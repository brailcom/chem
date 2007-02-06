import Pyro.core
from object_types import Value, Part, Complex, MultiView, Relation, PartMultiView, ValuePart
from data_types import DataTypeFactory
import oasa

class ChemReader:
    """class responsible for reading of chemical data and providing
    an internal representation of them.

    This one is a fake implementation that always returns the same object
    """

    @classmethod
    def process_string_old(self, g, format="SMILES"):
        """reads a molecular graph and creates the representation using data_types.

        NOTE: it does not read g for now - it uses the value of 'smiles' instead"""

        smiles = "Cc1ccccc1C=O"
        
        g = oasa.smiles.text_to_mol(smiles)

        root = Fork(type_id="ROOT", description="All data")
        str1 = Fork(type_id="STRUCTURE", description="Molecule 1")
        root.add_link(str1)

        str1.add_link(Value(g.get_mol_weight(), "MW", description="Molecular weight"))
        str1.add_link(Value(str(g.get_formula_dict()), "MF", description="Molecular formula"))

        frags = Complex("FRAGMENTS", description="Important fragments")
        str1.add_link(frags)

        fragment_class = PartComplexValue
        atom_class = ValuePart
        fs = []
        i = 0

        # this creates the fragments from predefined groups of atoms
        for indexes in [[0],[1,2,3,4,5,6],[7,8]]:
            i += 1
            f = fragment_class("FRAGMENT", description="Fragment %d" % i)
            fs.append(f)
            for j in indexes:
                f.add_part(atom_class(g.vertices[j].symbol, "ATOM", description="Atom %s" % g.vertices[j].symbol))

        values = ["methyl", "benzene", "carbonyl"]
        for i, f in enumerate(fs):
            frags.add_part(f)
            f.value = values[i]
            if i in [0,2]:
                f.add_neighbor(fs[1])  # f[0] and f[2] have f[1] as a neighbor
            elif i == 1:
                f.add_neighbor(fs[0])
                f.add_neighbor(fs[2])

        # this adds the atoms
        for v in g.vertices:
            v.properties_['data_mirror'] = atom_class(type_id="ATOM", description="atom", value=v.symbol)

        atoms = Complex("ATOMS", description="Atoms")
        str1.add_link(atoms)
        for v in g.vertices:
            a = v.properties_['data_mirror']
            for e,n in v.get_neighbor_edge_pairs():
                a.add_neighbor(n.properties_['data_mirror'], Relation(type_id="BOND", description="bond", value=e.order))
            atoms.add_part(a)

        return root


    bond_order_to_relation = {1: 'REL_SINGLE_BOND',
                              2: 'REL_DOUBLE_BOND',
                              3: 'REL_TRIPLE_BOND',
                              4: 'REL_AROMATIC_BOND'}


    @classmethod
    def process_string(self, g, format="SMILES"):
        """this fake method returns the reaction: CH3COOH + CH3OH -> CH3COOCH3"""
        # shortcut
        id2t = DataTypeFactory.data_type_from_id
        # the reaction
        root = MultiView(id2t("REACTION"))
        # the view of reaction as a Complex of molecules
        react = Complex(id2t("REACTION COMPONENTS"))
        root.add_view(react)
        reactants = [oasa.smiles.text_to_mol("HC(H)(H)C(=O)OH"), oasa.smiles.text_to_mol("HC(H)(H)OH")]
        products = [oasa.smiles.text_to_mol("HC(H)(H)C(=O)OC(H)(H)H")]
        data_reactants = []
        data_products = []
        for mol in reactants+products:
            # build molecule (CH3COOH)
            mol_data = PartMultiView(id2t("MOLECULE"))
            if mol in reactants:
                react.add_part(Relation(id2t("REL_REACTANT"), mol_data))
                data_reactants.append(mol_data)
            else:
                react.add_part(Relation(id2t("REL_PRODUCT"), mol_data))
                data_products.append(mol_data)
            # add different views
            mol_data.add_view(Value(id2t("MW"), mol.weight))
            mol_data.add_view(Value(id2t("SUM"), str(mol.get_formula_dict())))
            mol_data_frags = Complex(id2t("FRAGMENTS"))
            mol_data.add_view(mol_data_frags)
            mol_data_atoms = Complex(id2t("ATOMS"))
            mol_data.add_view(mol_data_atoms)
            _atom_to_a_data = {}
            for atom in mol.atoms:
                a_data = ValuePart(id2t("ATOM"), atom.symbol)
                _atom_to_a_data[atom] = a_data
                mol_data_atoms.add_part(Relation(id2t('REL_COMPOSED_FROM'), a_data))
            for atom in mol.atoms:
                a_data = _atom_to_a_data[atom]
                for e,n in atom.get_neighbor_edge_pairs():
                    a_data.add_neighbor(Relation(id2t(self.bond_order_to_relation[e.order]), _atom_to_a_data[n]))
        data_reactants[0].add_neighbor(Relation(id2t("REL_REACTS_WITH"), data_reactants[1]))
        data_reactants[1].add_neighbor(Relation(id2t("REL_REACTS_WITH"), data_reactants[0]))
        data_reactants[0].add_neighbor(Relation(id2t("REL_PRODUCES"), data_products[0]))
        data_reactants[1].add_neighbor(Relation(id2t("REL_PRODUCES"), data_products[0]))
        data_products[0].add_neighbor(Relation(id2t("REL_PRODUCED_FROM"), data_reactants[0]))
        data_products[0].add_neighbor(Relation(id2t("REL_PRODUCED_FROM"), data_reactants[1]))        
        return root
        
