# coding: utf-8

# EN:          electronegativity
# group:       english name of a group the element belongs to
# ATOM_WEIGHT: atomic weight
# NAME_EN:     english name
# NAME_CZ:     czech name
# NAME_LAT:    latin name
# ATOM_SYMBOL: atom symbol
# ORBITALS:    electron structure of occupied orbitals
# DESC:        short czech description of the element
# OX_NUMBERS:  oxidation numbers that the element usually has in compounds
# ROW:         number of row where the element resides in the periodic table
# COLUMN:      number of column where the element resides in the periodic table
#                  101-114 is used for lanthanoids and actionoids that are normally
#                  not shown as part of the table
# PROTON_NUMBER: number of protons, also the index in the table


symbol2properties = {
'H': { 'EN': 2.1, 'group': 'non-metals',
'ATOM_WEIGHT': 1.00794, 'NAME_LAT': u'hydrogenium', 'COLUMN': 1, 'ATOM_SYMBOL': u'H', 'ORBITALS': '1s1',
'OX_NUMBERS': [1, -1], 'NAME_CZ': u'vodík', 'PROTON_NUMBER': 1, 'ROW': 1, 'NAME_EN': u'hydrogen', 'DESC': u'bezbarvý plyn', },
'He': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 4.002602, 'NAME_LAT': u'helium', 'COLUMN': 18, 'ATOM_SYMBOL': u'He', 'ORBITALS': '1s2',
'OX_NUMBERS': [], 'NAME_CZ': u'helium', 'PROTON_NUMBER': 2, 'ROW': 1, 'NAME_EN': u'helium', 'DESC': u'bezbarvý inertní plyn', },
'Li': { 'EN': 0.98, 'group': 'alkali-metals',
'ATOM_WEIGHT': 6.941, 'NAME_LAT': u'lithium', 'COLUMN': 1, 'ATOM_SYMBOL': u'Li', 'ORBITALS': '1s2 2s1',
'OX_NUMBERS': [1], 'NAME_CZ': u'lithium', 'PROTON_NUMBER': 3, 'ROW': 2, 'NAME_EN': u'lithium', 'DESC': u'měkký lehký stříbrolesklý kov', },
'Be': { 'EN': 1.57, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 9.012182, 'NAME_LAT': u'beryllium', 'COLUMN': 2, 'ATOM_SYMBOL': u'Be', 'ORBITALS': '1s2 2s2',
'OX_NUMBERS': [2], 'NAME_CZ': u'beryllium', 'PROTON_NUMBER': 4, 'ROW': 2, 'NAME_EN': u'beryllium', 'DESC': u'lehký stříbrolesklý kov', },
'B': { 'EN': 2.04, 'group': 'non-metals',
'ATOM_WEIGHT': 10.811, 'NAME_LAT': u'borium', 'COLUMN': 13, 'ATOM_SYMBOL': u'B', 'ORBITALS': '1s2 2s2 2p1',
'OX_NUMBERS': [3], 'NAME_CZ': u'bor', 'PROTON_NUMBER': 5, 'ROW': 2, 'NAME_EN': u'boron', 'DESC': u'pevná látka', },
'C': { 'EN': 2.55, 'group': 'non-metals',
'ATOM_WEIGHT': 12.0107, 'NAME_LAT': u'carbonium', 'COLUMN': 14, 'ATOM_SYMBOL': u'C', 'ORBITALS': '1s2 2s2 2p2',
'OX_NUMBERS': [4, 2, -4], 'NAME_CZ': u'uhlík', 'PROTON_NUMBER': 6, 'ROW': 2, 'NAME_EN': u'carbon', 'DESC': u'měkký černý grafit, tvrdý bezbarvý diamant', },
'N': { 'EN': 3.04, 'group': 'non-metals',
'ATOM_WEIGHT': 14.0067, 'NAME_LAT': u'nitrogenium', 'COLUMN': 15, 'ATOM_SYMBOL': u'N', 'ORBITALS': '1s2 2s2 2p3',
'OX_NUMBERS': [5, 4, 3, 2, -3], 'NAME_CZ': u'dusík', 'PROTON_NUMBER': 7, 'ROW': 2, 'NAME_EN': u'nitrogen', 'DESC': u'bezbarvý inertní plyn', },
'O': { 'EN': 3.44, 'group': 'non-metals',
'ATOM_WEIGHT': 15.9994, 'NAME_LAT': u'oxygenium', 'COLUMN': 16, 'ATOM_SYMBOL': u'O', 'ORBITALS': '1s2 2s2 2p4',
'OX_NUMBERS': [-2, -1], 'NAME_CZ': u'kyslík', 'PROTON_NUMBER': 8, 'ROW': 2, 'NAME_EN': u'oxygen', 'DESC': u'reaktivní bezbarvý plyn', },
'F': { 'EN': 3.98, 'group': 'metals',
'ATOM_WEIGHT': 18.9984032, 'NAME_LAT': u'fluorum', 'COLUMN': 17, 'ATOM_SYMBOL': u'F', 'ORBITALS': '1s2 2s2 2p5',
'OX_NUMBERS': [-1], 'NAME_CZ': u'fluor', 'PROTON_NUMBER': 9, 'ROW': 2, 'NAME_EN': u'fluorine', 'DESC': u'reaktivní plyn', },
'Ne': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 20.1797, 'NAME_LAT': u'neon', 'COLUMN': 18, 'ATOM_SYMBOL': u'Ne', 'ORBITALS': '1s2 2s2 2p6',
'OX_NUMBERS': [], 'NAME_CZ': u'neon', 'PROTON_NUMBER': 10, 'ROW': 2, 'NAME_EN': u'neon', 'DESC': u'bezbarvý inertní plyn', },
'Na': { 'EN': 0.93, 'group': 'alkali-metals',
'ATOM_WEIGHT': 22.98977, 'NAME_LAT': u'natrium', 'COLUMN': 1, 'ATOM_SYMBOL': u'Na', 'ORBITALS': '1s2 2s2 2p6 3s1',
'OX_NUMBERS': [1], 'NAME_CZ': u'sodík', 'PROTON_NUMBER': 11, 'ROW': 3, 'NAME_EN': u'sodium', 'DESC': u'měkký stříbrolesklý kov', },
'Mg': { 'EN': 1.31, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 24.305, 'NAME_LAT': u'magnesium', 'COLUMN': 2, 'ATOM_SYMBOL': u'Mg', 'ORBITALS': '1s2 2s2 2p6 3s2',
'OX_NUMBERS': [2], 'NAME_CZ': u'hořčík', 'PROTON_NUMBER': 12, 'ROW': 3, 'NAME_EN': u'magnesium', 'DESC': u'měkký stříbrolesklý kov', },
'Al': { 'EN': 1.61, 'group': 'other-metals',
'ATOM_WEIGHT': 26.981538, 'NAME_LAT': u'aluminium', 'COLUMN': 13, 'ATOM_SYMBOL': u'Al', 'ORBITALS': '1s2 2s2 2p6 3s2 3p1',
'OX_NUMBERS': [3], 'NAME_CZ': u'hliník', 'PROTON_NUMBER': 13, 'ROW': 3, 'NAME_EN': u'aluminium', 'DESC': u'měkký stříbrošedý kov', },
'Si': { 'EN': 1.91, 'group': 'non-metals',
'ATOM_WEIGHT': 28.0855, 'NAME_LAT': u'silicium', 'COLUMN': 14, 'ATOM_SYMBOL': u'Si', 'ORBITALS': '1s2 2s2 2p6 3s2 3p2',
'OX_NUMBERS': [4, 2, -4], 'NAME_CZ': u'křemík', 'PROTON_NUMBER': 14, 'ROW': 3, 'NAME_EN': u'silicon', 'DESC': u'šedý tvrdý a křehký polokov', },
'P': { 'EN': 2.19, 'group': 'non-metals',
'ATOM_WEIGHT': 30.973761, 'NAME_LAT': u'phosphorus', 'COLUMN': 15, 'ATOM_SYMBOL': u'P', 'ORBITALS': '1s2 2s2 2p6 3s2 3p3',
'OX_NUMBERS': [5, 3, -3], 'NAME_CZ': u'fosfor', 'PROTON_NUMBER': 15, 'ROW': 3, 'NAME_EN': u'phosphorus', 'DESC': u'bílá, červená a černá modifikace', },
'S': { 'EN': 2.58, 'group': 'non-metals',
'ATOM_WEIGHT': 32.065, 'NAME_LAT': u'sulphurium', 'COLUMN': 16, 'ATOM_SYMBOL': u'S', 'ORBITALS': '1s2 2s2 2p6 3s2 3p4',
'OX_NUMBERS': [6, 4, 2, -2], 'NAME_CZ': u'síra', 'PROTON_NUMBER': 16, 'ROW': 3, 'NAME_EN': u'sulfur', 'DESC': u'žlutá krystalická látka', },
'Cl': { 'EN': 3.16, 'group': 'metals',
'ATOM_WEIGHT': 35.453, 'NAME_LAT': u'chlorium', 'COLUMN': 17, 'ATOM_SYMBOL': u'Cl', 'ORBITALS': '1s2 2s2 2p6 3s2 3p5',
'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'chlor', 'PROTON_NUMBER': 17, 'ROW': 3, 'NAME_EN': u'chlorine', 'DESC': u'reaktivní žlutozelený plyn', },
'Ar': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 39.948, 'NAME_LAT': u'argon', 'COLUMN': 18, 'ATOM_SYMBOL': u'Ar', 'ORBITALS': '1s2 2s2 2p6 3s2 3p6',
'OX_NUMBERS': [], 'NAME_CZ': u'argon', 'PROTON_NUMBER': 18, 'ROW': 3, 'NAME_EN': u'argon', 'DESC': u'bezbarvý inertní plyn', },
'K': { 'EN': 0.82, 'group': 'alkali-metals',
'ATOM_WEIGHT': 39.0983, 'NAME_LAT': u'kalium', 'COLUMN': 1, 'ATOM_SYMBOL': u'K', 'ORBITALS': 'Ar 4s1',
'OX_NUMBERS': [1], 'NAME_CZ': u'draslík', 'PROTON_NUMBER': 19, 'ROW': 4, 'NAME_EN': u'potassium', 'DESC': u'měkký stříbrolesklý kov', },
'Ca': { 'EN': 1.0, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 40.078, 'NAME_LAT': u'calcium', 'COLUMN': 2, 'ATOM_SYMBOL': u'Ca', 'ORBITALS': 'Ar 4s2',
'OX_NUMBERS': [2], 'NAME_CZ': u'vápník', 'PROTON_NUMBER': 20, 'ROW': 4, 'NAME_EN': u'calcium', 'DESC': u'měkký stříbrolesklý kov', },
'Sc': { 'EN': 1.36, 'group': 'metals',
'ATOM_WEIGHT': 44.95591, 'NAME_LAT': u'scandium', 'COLUMN': 3, 'ATOM_SYMBOL': u'Sc', 'ORBITALS': 'Ar 3d1 4s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'scandium', 'PROTON_NUMBER': 21, 'NAME_EN': u'scandium', 'ROW': 4, },
'Ti': { 'EN': 1.54, 'group': 'metals',
'ATOM_WEIGHT': 47.867, 'NAME_LAT': u'titanium', 'COLUMN': 4, 'ATOM_SYMBOL': u'Ti', 'ORBITALS': 'Ar 3d2 4s2',
'OX_NUMBERS': [4, 3, 2], 'NAME_CZ': u'titan', 'PROTON_NUMBER': 22, 'ROW': 4, 'NAME_EN': u'titanium', 'DESC': u'tvrdý a lehký stříbrolesklý kov', },
'V': { 'EN': 1.63, 'group': 'metals',
'ATOM_WEIGHT': 50.9415, 'NAME_LAT': u'vanadium', 'COLUMN': 5, 'ATOM_SYMBOL': u'V', 'ORBITALS': 'Ar 3d3 4s2',
'OX_NUMBERS': [5, 4, 3, 2, 1, 0, -1, -3], 'NAME_CZ': u'vanad', 'PROTON_NUMBER': 23, 'ROW': 4, 'NAME_EN': u'vanadium', 'DESC': u'tvrdý ocelově šedý kov', },
'Cr': { 'EN': 1.66, 'group': 'metals',
'ATOM_WEIGHT': 51.9961, 'NAME_LAT': u'chromium', 'COLUMN': 6, 'ATOM_SYMBOL': u'Cr', 'ORBITALS': 'Ar 3d5 4s1',
'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1, -2], 'NAME_CZ': u'chrom', 'PROTON_NUMBER': 24, 'ROW': 4, 'NAME_EN': u'chromium', 'DESC': u'tvrdý stříbrolesklý kov', },
'Mn': { 'EN': 1.55, 'group': 'metals',
'ATOM_WEIGHT': 54.938049, 'NAME_LAT': u'manganum', 'COLUMN': 7, 'ATOM_SYMBOL': u'Mn', 'ORBITALS': 'Ar 3d5 4s2',
'OX_NUMBERS': [7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3], 'NAME_CZ': u'mangan', 'PROTON_NUMBER': 25, 'ROW': 4, 'NAME_EN': u'manganese', 'DESC': u'tvrdý a křehký stříbrolesklý kov', },
'Fe': { 'EN': 1.83, 'group': 'metals',
'ATOM_WEIGHT': 55.845, 'NAME_LAT': u'ferrum', 'COLUMN': 8, 'ATOM_SYMBOL': u'Fe', 'ORBITALS': 'Ar 3d6 4s2',
'OX_NUMBERS': [6, 4, 5, 3, 2, 1, 0, -1, -2], 'NAME_CZ': u'železo', 'PROTON_NUMBER': 26, 'ROW': 4, 'NAME_EN': u'iron', 'DESC': u'stříbrolesklý kov', },
'Co': { 'EN': 1.88, 'group': 'metals',
'ATOM_WEIGHT': 58.9332, 'NAME_LAT': u'cobaltum', 'COLUMN': 9, 'ATOM_SYMBOL': u'Co', 'ORBITALS': 'Ar 3d7 4s2',
'OX_NUMBERS': [5, 4, 3, 2, 1, 0, -1], 'NAME_CZ': u'kobalt', 'PROTON_NUMBER': 27, 'ROW': 4, 'NAME_EN': u'cobalt', 'DESC': u'tvrdý stříbrošedý kov', },
'Ni': { 'EN': 1.91, 'group': 'metals',
'ATOM_WEIGHT': 58.6934, 'NAME_LAT': u'niccolum', 'COLUMN': 10, 'ATOM_SYMBOL': u'Ni', 'ORBITALS': 'Ar 3d8 4s2',
'OX_NUMBERS': [4, 3, 2, 1, 0, -1], 'NAME_CZ': u'nikl', 'PROTON_NUMBER': 28, 'ROW': 4, 'NAME_EN': u'nickel', 'DESC': u'bílý kov', },
'Cu': { 'EN': 1.9, 'group': 'metals',
'ATOM_WEIGHT': 63.546, 'NAME_LAT': u'cuprum', 'COLUMN': 11, 'ATOM_SYMBOL': u'Cu', 'ORBITALS': 'Ar 3d10 4s1',
'OX_NUMBERS': [4, 3, 2, 1], 'NAME_CZ': u'měď', 'PROTON_NUMBER': 29, 'ROW': 4, 'NAME_EN': u'copper', 'DESC': u'měkký načervenalý kov', },
'Zn': { 'EN': 1.65, 'group': 'metals',
'ATOM_WEIGHT': 65.39, 'NAME_LAT': u'zincum', 'COLUMN': 12, 'ATOM_SYMBOL': u'Zn', 'ORBITALS': 'Ar 3d10 4s2',
'OX_NUMBERS': [2], 'NAME_CZ': u'zinek', 'PROTON_NUMBER': 30, 'ROW': 4, 'NAME_EN': u'zinc', 'DESC': u'křehký modrobílý kov', },
'Ga': { 'EN': 1.81, 'group': 'other-metals',
'ATOM_WEIGHT': 69.723, 'NAME_LAT': u'gallium', 'COLUMN': 13, 'ATOM_SYMBOL': u'Ga', 'ORBITALS': 'Ar 3d10 4s2 4p1',
'OX_NUMBERS': [3, 2, 1], 'NAME_CZ': u'galium', 'PROTON_NUMBER': 31, 'ROW': 4, 'NAME_EN': u'gallium', 'DESC': u'měkký stříbrolesklý kov', },
'Ge': { 'EN': 2.01, 'group': 'other-metals',
'ATOM_WEIGHT': 72.64, 'NAME_LAT': u'germanium', 'COLUMN': 14, 'ATOM_SYMBOL': u'Ge', 'ORBITALS': 'Ar 3d10 4s2 4p2',
'OX_NUMBERS': [4, 2], 'NAME_CZ': u'germanium', 'PROTON_NUMBER': 32, 'ROW': 4, 'NAME_EN': u'germanium', 'DESC': u'lesklý šedobílý polokov', },
'As': { 'EN': 2.18, 'group': 'non-metals',
'ATOM_WEIGHT': 74.9216, 'NAME_LAT': u'arsenicum', 'COLUMN': 15, 'ATOM_SYMBOL': u'As', 'ORBITALS': 'Ar 3d10 4s2 4p3',
'OX_NUMBERS': [5, 3, -3], 'NAME_CZ': u'arsen', 'PROTON_NUMBER': 33, 'ROW': 4, 'NAME_EN': u'arsenic', 'DESC': u'lehký polokov', },
'Se': { 'EN': 2.55, 'group': 'non-metals',
'ATOM_WEIGHT': 78.96, 'NAME_LAT': u'selenium', 'COLUMN': 16, 'ATOM_SYMBOL': u'Se', 'ORBITALS': 'Ar 3d10 4s2 4p4',
'OX_NUMBERS': [6, 4, -2], 'NAME_CZ': u'selen', 'PROTON_NUMBER': 34, 'ROW': 4, 'NAME_EN': u'selenium', 'DESC': u'lesklý černošedý nekov', },
'Br': { 'EN': 2.96, 'group': 'metals',
'ATOM_WEIGHT': 79.904, 'NAME_LAT': u'bromium', 'COLUMN': 17, 'ATOM_SYMBOL': u'Br', 'ORBITALS': 'Ar 3d10 4s2 4p5',
'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'brom', 'PROTON_NUMBER': 35, 'ROW': 4, 'NAME_EN': u'bromine', 'DESC': u'reaktivní tmavě fialová kapalina', },
'Kr': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 83.8, 'NAME_LAT': u'krypton', 'COLUMN': 18, 'ATOM_SYMBOL': u'Kr', 'ORBITALS': 'Ar 3d10 4s2 4p6',
'OX_NUMBERS': [2], 'NAME_CZ': u'krypton', 'PROTON_NUMBER': 36, 'ROW': 4, 'NAME_EN': u'krypton', 'DESC': u'bezbarvý inertní plyn', },
'Rb': { 'EN': 0.82, 'group': 'alkali-metals',
'ATOM_WEIGHT': 85.4678, 'NAME_LAT': u'rubidium', 'COLUMN': 1, 'ATOM_SYMBOL': u'Rb', 'ORBITALS': 'Kr 5s1',
'OX_NUMBERS': [1], 'NAME_CZ': u'rubidium', 'PROTON_NUMBER': 37, 'ROW': 5, 'NAME_EN': u'rubidium', 'DESC': u'reaktivní měkký a lehký stříbrolesklý kov', },
'Sr': { 'EN': 0.95, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 87.62, 'NAME_LAT': u'strontium', 'COLUMN': 2, 'ATOM_SYMBOL': u'Sr', 'ORBITALS': 'Kr 5s2',
'OX_NUMBERS': [2], 'NAME_CZ': u'stroncium', 'PROTON_NUMBER': 38, 'ROW': 5, 'NAME_EN': u'strontium', 'DESC': u'stříbrolesklý kov', },
'Y': { 'EN': 1.22, 'group': 'metals',
'ATOM_WEIGHT': 88.90585, 'NAME_LAT': u'yttrium', 'COLUMN': 3, 'ATOM_SYMBOL': u'Y', 'ORBITALS': 'Kr 4d1 5s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'yttrium', 'PROTON_NUMBER': 39, 'NAME_EN': u'yttrium', 'ROW': 5, },
'Zr': { 'EN': 1.33, 'group': 'metals',
'ATOM_WEIGHT': 91.224, 'NAME_LAT': u'zirconium', 'COLUMN': 4, 'ATOM_SYMBOL': u'Zr', 'ORBITALS': 'Kr 4d2 5s2',
'OX_NUMBERS': [4, 3, 2, 1], 'NAME_CZ': u'zirkon', 'PROTON_NUMBER': 40, 'ROW': 5, 'NAME_EN': u'zirconium', 'DESC': u'látka stříbrošedý kov', },
'Nb': { 'EN': 1.6, 'group': 'metals',
'ATOM_WEIGHT': 92.90638, 'NAME_LAT': u'niobium', 'COLUMN': 5, 'ATOM_SYMBOL': u'Nb', 'ORBITALS': 'Kr 4d4',
'OX_NUMBERS': [5, 4, 3, 2, 1, -1], 'NAME_CZ': u'niob', 'PROTON_NUMBER': 41, 'NAME_EN': u'niobium', 'ROW': 5, },
'Mo': { 'EN': 2.16, 'group': 'metals',
'ATOM_WEIGHT': 95.94, 'NAME_LAT': u'molybdenum', 'COLUMN': 6, 'ATOM_SYMBOL': u'Mo', 'ORBITALS': 'Kr 4d5 5s1',
'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1, -2], 'NAME_CZ': u'molybden', 'PROTON_NUMBER': 42, 'ROW': 5, 'NAME_EN': u'molybdenum', 'DESC': u'stříbrolesklý kov', },
'Tc': { 'EN': 1.9, 'group': 'metals',
'ATOM_WEIGHT': 98.9063, 'NAME_LAT': u'technetium', 'COLUMN': 7, 'ATOM_SYMBOL': u'Tc', 'ORBITALS': 'Kr 4d6 5s1',
'OX_NUMBERS': [7, 6, 5, 4, 3, 2, 1, 0, -1, -3], 'NAME_CZ': u'technecium', 'PROTON_NUMBER': 43, 'NAME_EN': u'technetium', 'ROW': 5, },
'Ru': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 101.07, 'NAME_LAT': u'ruthenium', 'COLUMN': 8, 'ATOM_SYMBOL': u'Ru', 'ORBITALS': 'Kr 4d7 5s1',
'OX_NUMBERS': [8, 7, 6, 5, 4, 3, 2, 1, 0, -2], 'NAME_CZ': u'ruthenium', 'PROTON_NUMBER': 44, 'ROW': 5, 'NAME_EN': u'ruthenium', 'DESC': u'šedý a tvrdý ušlechtilý kov', },
'Rh': { 'EN': 2.28, 'group': 'metals',
'ATOM_WEIGHT': 102.9055, 'NAME_LAT': u'rhodium', 'COLUMN': 9, 'ATOM_SYMBOL': u'Rh', 'ORBITALS': 'Kr 4d8 5s1',
'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1], 'NAME_CZ': u'rhodium', 'PROTON_NUMBER': 45, 'ROW': 5, 'NAME_EN': u'rhodium', 'DESC': u'bezbarvý tažný kov', },
'Pd': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 106.42, 'NAME_LAT': u'palladium', 'COLUMN': 10, 'ATOM_SYMBOL': u'Pd', 'ORBITALS': 'Kr 4d10',
'OX_NUMBERS': [4, 3, 2, 0], 'NAME_CZ': u'palladium', 'PROTON_NUMBER': 46, 'ROW': 5, 'NAME_EN': u'palladium', 'DESC': u'kujný a tažný stříbrolesklý kov', },
'Ag': { 'EN': 1.93, 'group': 'metals',
'ATOM_WEIGHT': 107.8682, 'NAME_LAT': u'argentum', 'COLUMN': 11, 'ATOM_SYMBOL': u'Ag', 'ORBITALS': 'Kr 4d10 5s1',
'OX_NUMBERS': [3, 2, 1], 'NAME_CZ': u'stříbro', 'PROTON_NUMBER': 47, 'ROW': 5, 'NAME_EN': u'silver', 'DESC': u'měkký stříbrolesklý kov', },
'Cd': { 'EN': 1.69, 'group': 'metals',
'ATOM_WEIGHT': 112.411, 'NAME_LAT': u'cadmium', 'COLUMN': 12, 'ATOM_SYMBOL': u'Cd', 'ORBITALS': 'Kr 4d10 5s2',
'OX_NUMBERS': [2, 1], 'NAME_CZ': u'kadmium', 'PROTON_NUMBER': 48, 'ROW': 5, 'NAME_EN': u'cadmium', 'DESC': u'bezbarvý tažný kov', },
'In': { 'EN': 1.78, 'group': 'other-metals',
'ATOM_WEIGHT': 114.818, 'NAME_LAT': u'indium', 'COLUMN': 13, 'ATOM_SYMBOL': u'In', 'ORBITALS': 'Kr 4d10 5s2 5p1',
'OX_NUMBERS': [3, 2, 1], 'NAME_CZ': u'indium', 'PROTON_NUMBER': 49, 'NAME_EN': u'indium', 'ROW': 5, },
'Sn': { 'EN': 1.96, 'group': 'other-metals',
'ATOM_WEIGHT': 118.71, 'NAME_LAT': u'stannum', 'COLUMN': 14, 'ATOM_SYMBOL': u'Sn', 'ORBITALS': 'Kr 4d10 5s2 5p2',
'OX_NUMBERS': [4, 2], 'NAME_CZ': u'cín', 'PROTON_NUMBER': 50, 'ROW': 5, 'NAME_EN': u'tin', 'DESC': u'měkký stříbrolesklý kov', },
'Sb': { 'EN': 2.05, 'group': 'other-metals',
'ATOM_WEIGHT': 121.76, 'NAME_LAT': u'stibium', 'COLUMN': 15, 'ATOM_SYMBOL': u'Sb', 'ORBITALS': 'Kr 4d10 5s2 5p3',
'OX_NUMBERS': [5, 3, -3], 'NAME_CZ': u'antimon', 'PROTON_NUMBER': 51, 'ROW': 5, 'NAME_EN': u'antimony', 'DESC': u'stříbrolesklý křehký polokov', },
'Te': { 'EN': 2.1, 'group': 'non-metals',
'ATOM_WEIGHT': 127.6, 'NAME_LAT': u'tellurium', 'COLUMN': 16, 'ATOM_SYMBOL': u'Te', 'ORBITALS': 'Kr 4d10 5s2 5p4',
'OX_NUMBERS': [6, 4, 2, -2], 'NAME_CZ': u'tellur', 'PROTON_NUMBER': 52, 'ROW': 5, 'NAME_EN': u'tellurium', 'DESC': u'stříbrolesklý polokov', },
'I': { 'EN': 2.66, 'group': 'metals',
'ATOM_WEIGHT': 126.90447, 'NAME_LAT': u'iodium', 'COLUMN': 17, 'ATOM_SYMBOL': u'I', 'ORBITALS': 'Kr 4d10 5s2 5p5',
'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'jod', 'PROTON_NUMBER': 53, 'ROW': 5, 'NAME_EN': u'iodine', 'DESC': u'reaktivní tmavě fialová pevná látka', },
'Xe': { 'EN': 2.6, 'group': 'inert-gases',
'ATOM_WEIGHT': 131.293, 'NAME_LAT': u'xenon', 'COLUMN': 18, 'ATOM_SYMBOL': u'Xe', 'ORBITALS': 'Kr 4d10 5s2 5p6',
'OX_NUMBERS': [2, 4, 6, 8], 'NAME_CZ': u'xenon', 'PROTON_NUMBER': 54, 'ROW': 5, 'NAME_EN': u'xenon', 'DESC': u'bezbarvý inertní plyn', },
'Cs': { 'EN': 0.79, 'group': 'alkali-metals',
'ATOM_WEIGHT': 132.90545, 'NAME_LAT': u'caesium', 'COLUMN': 1, 'ATOM_SYMBOL': u'Cs', 'ORBITALS': 'Xe 6s1',
'OX_NUMBERS': [1], 'NAME_CZ': u'cesium', 'PROTON_NUMBER': 55, 'ROW': 6, 'NAME_EN': u'caesium', 'DESC': u'reaktivní měkký a lehký stříbrolesklý kov', },
'Ba': { 'EN': 0.89, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 137.237, 'NAME_LAT': u'barium', 'COLUMN': 2, 'ATOM_SYMBOL': u'Ba', 'ORBITALS': 'Xe 6s2',
'OX_NUMBERS': [2], 'NAME_CZ': u'barium', 'PROTON_NUMBER': 56, 'ROW': 6, 'NAME_EN': u'barium', 'DESC': u'měkký stříbrolesklý kov', },
'La': { 'EN': 1.1, 'group': 'metals',
'ATOM_WEIGHT': 138.9055, 'NAME_LAT': u'lanthanum', 'COLUMN': 101, 'ATOM_SYMBOL': u'La', 'ORBITALS': 'Xe 5d1 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'lanthan', 'PROTON_NUMBER': 57, 'NAME_EN': u'lanthanum', 'ROW': 6, },
'Ce': { 'EN': 1.12, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 140.116, 'NAME_LAT': u'cerium', 'COLUMN': 102, 'ATOM_SYMBOL': u'Ce', 'ORBITALS': 'Xe 4f1 5d1 6s2',
'OX_NUMBERS': [4, 3], 'NAME_CZ': u'cer', 'PROTON_NUMBER': 58, 'NAME_EN': u'cerium', 'ROW': 6, },
'Pr': { 'EN': 1.13, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 140.90765, 'NAME_LAT': u'praseodymium', 'COLUMN': 103, 'ATOM_SYMBOL': u'Pr', 'ORBITALS': 'Xe 4f3 6s2',
'OX_NUMBERS': [4, 3], 'NAME_CZ': u'praseodym', 'PROTON_NUMBER': 59, 'NAME_EN': u'praseodymium', 'ROW': 6, },
'Nd': { 'EN': 1.14, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 144.24, 'NAME_LAT': u'neodymium', 'COLUMN': 104, 'ATOM_SYMBOL': u'Nd', 'ORBITALS': 'Xe 4f4 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'neodym', 'PROTON_NUMBER': 60, 'NAME_EN': u'neodymium', 'ROW': 6, },
'Pm': { 'EN': 1.13, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 146.9151, 'NAME_LAT': u'promethium', 'COLUMN': 105, 'ATOM_SYMBOL': u'Pm', 'ORBITALS': 'Xe 4f5 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'promethium', 'PROTON_NUMBER': 61, 'NAME_EN': u'promethium', 'ROW': 6, },
'Sm': { 'EN': 1.17, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 150.36, 'NAME_LAT': u'samarium', 'COLUMN': 106, 'ATOM_SYMBOL': u'Sm', 'ORBITALS': 'Xe 4f6 6s2',
'OX_NUMBERS': [3, 2], 'NAME_CZ': u'samarium', 'PROTON_NUMBER': 62, 'NAME_EN': u'samarium', 'ROW': 6, },
'Eu': { 'EN': 1.2, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 151.964, 'NAME_LAT': u'europium', 'COLUMN': 107, 'ATOM_SYMBOL': u'Eu', 'ORBITALS': 'Xe 4f7 6s2',
'OX_NUMBERS': [3, 2], 'NAME_CZ': u'europium', 'PROTON_NUMBER': 63, 'NAME_EN': u'europium', 'ROW': 6, },
'Gd': { 'EN': 1.2, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 157.25, 'NAME_LAT': u'gadolinium', 'COLUMN': 108, 'ATOM_SYMBOL': u'Gd', 'ORBITALS': 'Xe 4f7 5d1 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'gadolinium', 'PROTON_NUMBER': 64, 'NAME_EN': u'gadolinium', 'ROW': 6, },
'Tb': { 'EN': 1.1, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 158.92534, 'NAME_LAT': u'terbium', 'COLUMN': 109, 'ATOM_SYMBOL': u'Tb', 'ORBITALS': 'Xe 4f9 6s2',
'OX_NUMBERS': [4, 3], 'NAME_CZ': u'terbium', 'PROTON_NUMBER': 65, 'NAME_EN': u'terbium', 'ROW': 6, },
'Dy': { 'EN': 1.22, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 162.5, 'NAME_LAT': u'dysprosium', 'COLUMN': 110, 'ATOM_SYMBOL': u'Dy', 'ORBITALS': 'Xe 4f10 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'dysprosium', 'PROTON_NUMBER': 66, 'NAME_EN': u'dysprosium', 'ROW': 6, },
'Ho': { 'EN': 1.23, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 164.93032, 'NAME_LAT': u'holmium', 'COLUMN': 111, 'ATOM_SYMBOL': u'Ho', 'ORBITALS': 'Xe 4f11 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'holmium', 'PROTON_NUMBER': 67, 'NAME_EN': u'holmium', 'ROW': 6, },
'Er': { 'EN': 1.24, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 167.259, 'NAME_LAT': u'erbium', 'COLUMN': 112, 'ATOM_SYMBOL': u'Er', 'ORBITALS': 'Xe 4f12 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'erbium', 'PROTON_NUMBER': 68, 'NAME_EN': u'erbium', 'ROW': 6, },
'Tm': { 'EN': 1.25, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 168.93421, 'NAME_LAT': u'thulium', 'COLUMN': 113, 'ATOM_SYMBOL': u'Tm', 'ORBITALS': 'Xe 4f13 6s2',
'OX_NUMBERS': [3, 2], 'NAME_CZ': u'thulium', 'PROTON_NUMBER': 69, 'NAME_EN': u'thulium', 'ROW': 6, },
'Yb': { 'EN': 1.1, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 173.04, 'NAME_LAT': u'ytterbium', 'COLUMN': 114, 'ATOM_SYMBOL': u'Yb', 'ORBITALS': 'Xe 4f14 6s2',
'OX_NUMBERS': [3, 2], 'NAME_CZ': u'ytterbium', 'PROTON_NUMBER': 70, 'NAME_EN': u'ytterbium', 'ROW': 6, },
'Lu': { 'EN': 1.27, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 174.967, 'NAME_LAT': u'lutetium', 'COLUMN': 3, 'ATOM_SYMBOL': u'Lu', 'ORBITALS': 'Xe 4f14 5d1 6s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'lutecium', 'PROTON_NUMBER': 71, 'NAME_EN': u'lutetium', 'ROW': 6, },
'Hf': { 'EN': 1.3, 'group': 'metals',
'ATOM_WEIGHT': 178.49, 'NAME_LAT': u'hafnium', 'COLUMN': 4, 'ATOM_SYMBOL': u'Hf', 'ORBITALS': 'Xe 4f14 5d2 6s2',
'OX_NUMBERS': [4, 3, 1], 'NAME_CZ': u'hafnium', 'PROTON_NUMBER': 72, 'NAME_EN': u'hafnium', 'ROW': 6, },
'Ta': { 'EN': 1.5, 'group': 'metals',
'ATOM_WEIGHT': 180.9479, 'NAME_LAT': u'tantalum', 'COLUMN': 5, 'ATOM_SYMBOL': u'Ta', 'ORBITALS': 'Xe 4f14 5d3 6s2',
'OX_NUMBERS': [5, 4, 3, 2, 1, -1], 'NAME_CZ': u'tantal', 'PROTON_NUMBER': 73, 'NAME_EN': u'tantalum', 'ROW': 6, },
'W': { 'EN': 2.36, 'group': 'metals',
'ATOM_WEIGHT': 183.84, 'NAME_LAT': u'wolframium', 'COLUMN': 6, 'ATOM_SYMBOL': u'W', 'ORBITALS': 'Xe 4f14 5d4 6s2',
'OX_NUMBERS': [6, 5, 4, 3, 2, 0, -1, -2], 'NAME_CZ': u'wolfram', 'PROTON_NUMBER': 74, 'ROW': 6, 'NAME_EN': u'tungsten', 'DESC': u'stříbrolesklý kov', },
'Re': { 'EN': 1.9, 'group': 'metals',
'ATOM_WEIGHT': 186.207, 'NAME_LAT': u'rhenium', 'COLUMN': 7, 'ATOM_SYMBOL': u'Re', 'ORBITALS': 'Xe 4f14 5d5 6s2',
'OX_NUMBERS': [7, 6, 5, 4, 3, 2, 1, 0, -1, -3], 'NAME_CZ': u'rhenium', 'PROTON_NUMBER': 75, 'ROW': 6, 'NAME_EN': u'rhenium', 'DESC': u'měkký kujný kov', },
'Os': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 190.23, 'NAME_LAT': u'osmium', 'COLUMN': 8, 'ATOM_SYMBOL': u'Os', 'ORBITALS': 'Xe 4f14 5d6 6s2',
'OX_NUMBERS': [8, 6, 5, 4, 3, 2, 1, 0, -2], 'NAME_CZ': u'osmium', 'PROTON_NUMBER': 76, 'ROW': 6, 'NAME_EN': u'osmium', 'DESC': u'modrošedý kov', },
'Ir': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 192.217, 'NAME_LAT': u'iridium', 'COLUMN': 9, 'ATOM_SYMBOL': u'Ir', 'ORBITALS': 'Xe 4f14 5d7 6s2',
'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1], 'NAME_CZ': u'iridium', 'PROTON_NUMBER': 77, 'ROW': 6, 'NAME_EN': u'iridium', 'DESC': u'bílý tvrdý a křehký kov', },
'Pt': { 'EN': 2.28, 'group': 'metals',
'ATOM_WEIGHT': 195.078, 'NAME_LAT': u'platinum', 'COLUMN': 10, 'ATOM_SYMBOL': u'Pt', 'ORBITALS': 'Xe 4f14 5d9 6s1',
'OX_NUMBERS': [6, 5, 4, 2, 0], 'NAME_CZ': u'platina', 'PROTON_NUMBER': 78, 'ROW': 6, 'NAME_EN': u'platinum', 'DESC': u'stříbrolesklý kov', },
'Au': { 'EN': 2.54, 'group': 'metals',
'ATOM_WEIGHT': 196.96654, 'NAME_LAT': u'aurum', 'COLUMN': 11, 'ATOM_SYMBOL': u'Au', 'ORBITALS': 'Xe 4f14 5d10 6s1',
'OX_NUMBERS': [5, 3, 2, 1], 'NAME_CZ': u'zlato', 'PROTON_NUMBER': 79, 'ROW': 6, 'NAME_EN': u'gold', 'DESC': u'měkký žlutý kov', },
'Hg': { 'EN': 2.0, 'group': 'metals',
'ATOM_WEIGHT': 200.59, 'NAME_LAT': u'hydrargyrum', 'COLUMN': 12, 'ATOM_SYMBOL': u'Hg', 'ORBITALS': 'Xe 4f14 5d10 6s2',
'OX_NUMBERS': [2, 1], 'NAME_CZ': u'rtuť', 'PROTON_NUMBER': 80, 'ROW': 6, 'NAME_EN': u'mercury', 'DESC': u'stříbrolesklý kapalný kov', },
'Tl': { 'EN': 2.04, 'group': 'other-metals',
'ATOM_WEIGHT': 204.3833, 'NAME_LAT': u'thallium', 'COLUMN': 13, 'ATOM_SYMBOL': u'Tl', 'ORBITALS': 'Xe 4f14 5d10 6s2 6p1',
'OX_NUMBERS': [3, 1], 'NAME_CZ': u'thallium', 'PROTON_NUMBER': 81, 'ROW': 6, 'NAME_EN': u'thallium', 'DESC': u'měkký šedý kov', },
'Pb': { 'EN': 2.33, 'group': 'other-metals',
'ATOM_WEIGHT': 207.2, 'NAME_LAT': u'plumbum', 'COLUMN': 14, 'ATOM_SYMBOL': u'Pb', 'ORBITALS': 'Xe 4f14 5d10 6s2 6p2',
'OX_NUMBERS': [4, 2], 'NAME_CZ': u'olovo', 'PROTON_NUMBER': 82, 'ROW': 6, 'NAME_EN': u'lead', 'DESC': u'měkký šedý kov', },
'Bi': { 'EN': 2.02, 'group': 'other-metals',
'ATOM_WEIGHT': 208.98038, 'NAME_LAT': u'bisemutum', 'COLUMN': 15, 'ATOM_SYMBOL': u'Bi', 'ORBITALS': 'Xe 4f14 5d10 6s2 6p3',
'OX_NUMBERS': [5, 3], 'NAME_CZ': u'bismut', 'PROTON_NUMBER': 83, 'ROW': 6, 'NAME_EN': u'bismuth', 'DESC': u'lesklý narůžovělý kov', },
'Po': { 'EN': 2.0, 'group': 'other-metals',
'ATOM_WEIGHT': 208.9824, 'NAME_LAT': u'polonium', 'COLUMN': 16, 'ATOM_SYMBOL': u'Po', 'ORBITALS': 'Xe 4f14 5d10 6s2 6p4',
'OX_NUMBERS': [6, 4, 2], 'NAME_CZ': u'polonium', 'PROTON_NUMBER': 84, 'NAME_EN': u'polonium', 'ROW': 6, },
'At': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 209.9871, 'NAME_LAT': u'astatium', 'COLUMN': 17, 'ATOM_SYMBOL': u'At', 'ORBITALS': 'Xe 4f14 5d10 6s2 6p5',
'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'astat', 'PROTON_NUMBER': 85, 'NAME_EN': u'astatine', 'ROW': 6, },
'Rn': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 222.0176, 'NAME_LAT': u'radon', 'COLUMN': 18, 'ATOM_SYMBOL': u'Rn', 'ORBITALS': 'Xe 4f14 5d10 6s2 6p6',
'OX_NUMBERS': [2], 'NAME_CZ': u'radon', 'PROTON_NUMBER': 86, 'ROW': 6, 'NAME_EN': u'radon', 'DESC': u'bezbarvý radioaktivní inertní plyn', },
'Fr': { 'EN': 0.7, 'group': 'alkali-metals',
'ATOM_WEIGHT': 223.0197, 'NAME_LAT': u'francium', 'COLUMN': 1, 'ATOM_SYMBOL': u'Fr', 'ORBITALS': 'Rd 7s1',
'OX_NUMBERS': [1], 'NAME_CZ': u'francium', 'PROTON_NUMBER': 87, 'NAME_EN': u'francium', 'ROW': 7, },
'Ra': { 'EN': 0.89, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 226.0254, 'NAME_LAT': u'radium', 'COLUMN': 2, 'ATOM_SYMBOL': u'Ra', 'ORBITALS': 'Rd 7s2',
'OX_NUMBERS': [2], 'NAME_CZ': u'radium', 'PROTON_NUMBER': 88, 'ROW': 7, 'NAME_EN': u'radium', 'DESC': u'stříbrolesklý radioaktivní kov', },
'Ac': { 'EN': 1.1, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 227.0278, 'NAME_LAT': u'actinium', 'COLUMN': 101, 'ATOM_SYMBOL': u'Ac', 'ORBITALS': 'Rd 6d1 7s2',
'OX_NUMBERS': [3], 'NAME_CZ': u'actinium', 'PROTON_NUMBER': 89, 'NAME_EN': u'actinium', 'ROW': 7, },
'Th': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 232.0381, 'NAME_LAT': u'thorium', 'COLUMN': 102, 'ATOM_SYMBOL': u'Th', 'OX_NUMBERS': [4, 3, 2], 'NAME_CZ': u'thorium', 'PROTON_NUMBER': 90, 'NAME_EN': u'thorium', 'ROW': 7, },
'Pa': { 'EN': 1.5, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 231.03588, 'NAME_LAT': u'protactinium', 'COLUMN': 103, 'ATOM_SYMBOL': u'Pa', 'OX_NUMBERS': [5, 4, 3], 'NAME_CZ': u'protactinium', 'PROTON_NUMBER': 91, 'NAME_EN': u'protactinium', 'ROW': 7, },
'U': { 'EN': 1.38, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 238.02891, 'NAME_LAT': u'uranium', 'COLUMN': 104, 'ATOM_SYMBOL': u'U', 'OX_NUMBERS': [6, 5, 4, 3], 'NAME_CZ': u'uran', 'PROTON_NUMBER': 92, 'ROW': 7, 'NAME_EN': u'uranium', 'DESC': u'těžký stříbrošedý radioaktivní kov', },
'Np': { 'EN': 1.36, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 237.0482, 'NAME_LAT': u'neptunium', 'COLUMN': 105, 'ATOM_SYMBOL': u'Np', 'OX_NUMBERS': [7, 6, 5, 4, 3], 'NAME_CZ': u'neptunium', 'PROTON_NUMBER': 93, 'NAME_EN': u'neptunium', 'ROW': 7, },
'Pu': { 'EN': 1.28, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 244.0642, 'NAME_LAT': u'plutonium', 'COLUMN': 106, 'ATOM_SYMBOL': u'Pu', 'OX_NUMBERS': [7, 6, 5, 4, 3], 'NAME_CZ': u'plutonium', 'PROTON_NUMBER': 94, 'NAME_EN': u'plutonium', 'ROW': 7, },
'Am': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 243.0614, 'NAME_LAT': u'americium', 'COLUMN': 107, 'ATOM_SYMBOL': u'Am', 'OX_NUMBERS': [6, 5, 4, 3], 'NAME_CZ': u'americium', 'PROTON_NUMBER': 95, 'NAME_EN': u'americium', 'ROW': 7, },
'Cm': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 247.0703, 'NAME_LAT': u'curium', 'COLUMN': 108, 'ATOM_SYMBOL': u'Cm', 'OX_NUMBERS': [4, 3], 'NAME_CZ': u'curium', 'PROTON_NUMBER': 96, 'NAME_EN': u'curium', 'ROW': 7, },
'Bk': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 247.0703, 'NAME_LAT': u'berkelium', 'COLUMN': 109, 'ATOM_SYMBOL': u'Bk', 'OX_NUMBERS': [4, 3], 'NAME_CZ': u'berkelium', 'PROTON_NUMBER': 97, 'NAME_EN': u'berkelium', 'ROW': 7, },
'Cf': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 251.0796, 'NAME_LAT': u'californium', 'COLUMN': 110, 'ATOM_SYMBOL': u'Cf', 'OX_NUMBERS': [4, 3], 'NAME_CZ': u'californium', 'PROTON_NUMBER': 98, 'NAME_EN': u'californium', 'ROW': 7, },
'Es': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 252.0829, 'NAME_LAT': u'einsteinium', 'COLUMN': 111, 'ATOM_SYMBOL': u'Es', 'OX_NUMBERS': [3], 'NAME_CZ': u'einsteinium', 'PROTON_NUMBER': 99, 'NAME_EN': u'einsteinium', 'ROW': 7, },
'Fm': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 257.0951, 'NAME_LAT': u'fermium', 'COLUMN': 112, 'ATOM_SYMBOL': u'Fm', 'OX_NUMBERS': [3], 'NAME_CZ': u'fermium', 'PROTON_NUMBER': 100, 'NAME_EN': u'fermium', 'ROW': 7, },
'Md': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 258.0986, 'NAME_LAT': u'mendelevium', 'COLUMN': 113, 'ATOM_SYMBOL': u'Md', 'OX_NUMBERS': [3], 'NAME_CZ': u'mendelevium', 'PROTON_NUMBER': 101, 'NAME_EN': u'mendelevium', 'ROW': 7, },
'No': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 259.1009, 'NAME_LAT': u'nobelium', 'COLUMN': 114, 'ATOM_SYMBOL': u'No', 'OX_NUMBERS': [3, 2], 'NAME_CZ': u'nobelium', 'PROTON_NUMBER': 102, 'NAME_EN': u'nobelium', 'ROW': 7, },
'Lr': { 'EN': 1.3, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 262.11, 'NAME_LAT': u'lawrencium', 'COLUMN': 3, 'ATOM_SYMBOL': u'Lr', 'OX_NUMBERS': [3], 'NAME_CZ': u'lawrencium', 'PROTON_NUMBER': 103, 'NAME_EN': u'lawrencium', 'ROW': 7, },
'Rf': { 'EN': 0.0, 'group': 'metals',
'ATOM_WEIGHT': 261.1089, 'NAME_LAT': u'rutherfordium', 'COLUMN': 4, 'ATOM_SYMBOL': u'Rf', 'OX_NUMBERS': [], 'NAME_CZ': u'rutherfordium', 'PROTON_NUMBER': 104, 'NAME_EN': u'rutherfordium', 'ROW': 7, },
'Db': { 'EN': 0.0, 'group': 'metals',
'ATOM_WEIGHT': 262.1144, 'NAME_LAT': u'dubnium', 'COLUMN': 5, 'ATOM_SYMBOL': u'Db', 'ORBITALS': 'Rn 5f14 6d3 7s2',
'OX_NUMBERS': [], 'NAME_CZ': u'dubnium', 'PROTON_NUMBER': 105, 'NAME_EN': u'dubnium', 'ROW': 7, },
'Sg': { 'EN': 0.0, 'group': 'metals',
'ATOM_WEIGHT': 263.1186, 'NAME_LAT': u'seaborgium', 'COLUMN': 6, 'ATOM_SYMBOL': u'Sg', 'OX_NUMBERS': [], 'NAME_CZ': u'seaborgium', 'PROTON_NUMBER': 106, 'NAME_EN': u'seaborgium', 'ROW': 7, },
'Bh': { 'EN': 0.0, 'group': 'metals',
'ATOM_WEIGHT': 262.1231, 'NAME_LAT': u'bohrium', 'COLUMN': 7, 'ATOM_SYMBOL': u'Bh', 'OX_NUMBERS': [], 'NAME_CZ': u'bohrium', 'PROTON_NUMBER': 107, 'NAME_EN': u'bohrium', 'ROW': 7, },
'Hs': { 'EN': 0.0, 'group': 'metals',
'ATOM_WEIGHT': 265.1306, 'NAME_LAT': u'hassium', 'COLUMN': 8, 'ATOM_SYMBOL': u'Hs', 'OX_NUMBERS': [], 'NAME_CZ': u'hassium', 'PROTON_NUMBER': 108, 'NAME_EN': u'hassium', 'ROW': 7, },
'Mt': { 'EN': 0.0, 'group': 'metals',
'ATOM_WEIGHT': 266.1378, 'NAME_LAT': u'meitnerium', 'COLUMN': 9, 'ATOM_SYMBOL': u'Mt', 'OX_NUMBERS': [], 'NAME_CZ': u'meitnerium', 'PROTON_NUMBER': 109, 'NAME_EN': u'meitnerium', 'ROW': 7, },
}
