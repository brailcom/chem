# coding: utf-8
symbol2properties = {
'H': { 'EN': 2.1, 'group': 'non-metals',
'ATOM_WEIGHT': 1.0079, 'valency': (1,), 'ATOM_SYMBOL': u'H', 'NAME_LAT': u'hydrogenium', 'OX_NUMBERS': [1, -1], 'NAME_CZ': u'vodík', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 1, 'NAME_EN': u'hydrogen', 'DESC': u'bezbarvý plyn', },
'He': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 4.0026, 'valency': (0, 2), 'ATOM_SYMBOL': u'He', 'NAME_LAT': u'helium', 'OX_NUMBERS': [], 'NAME_CZ': u'helium', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 2, 'NAME_EN': u'helium', 'DESC': u'bezbarvý inertní plyn', },
'Cu': { 'EN': 1.9, 'group': 'metals',
'ATOM_WEIGHT': 63.546, 'valency': (2, 1), 'ATOM_SYMBOL': u'Cu', 'NAME_LAT': u'cuprum', 'OX_NUMBERS': [4, 3, 2, 1], 'NAME_CZ': u'měď', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 29, 'NAME_EN': u'copper', 'DESC': u'měkký načervenalý kov', },
'Na': { 'EN': 0.93, 'group': 'alkali-metals',
'ATOM_WEIGHT': 22.9898, 'valency': (1,), 'ATOM_SYMBOL': u'Na', 'NAME_LAT': u'natrium', 'OX_NUMBERS': [1], 'NAME_CZ': u'sodík', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 11, 'NAME_EN': u'sodium', 'DESC': u'měkký stříbrolesklý kov', },
'K': { 'EN': 0.82, 'group': 'alkali-metals',
'ATOM_WEIGHT': 39.0983, 'valency': (1,), 'ATOM_SYMBOL': u'K', 'NAME_LAT': u'kalium', 'OX_NUMBERS': [1], 'NAME_CZ': u'draslík', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 19, 'NAME_EN': u'potassium', 'DESC': u'měkký stříbrolesklý kov', },
'Mg': { 'EN': 1.31, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 24.305, 'valency': (2,), 'ATOM_SYMBOL': u'Mg', 'NAME_LAT': u'magnesium', 'OX_NUMBERS': [2], 'NAME_CZ': u'hořčík', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 12, 'NAME_EN': u'magnesium', 'DESC': u'měkký stříbrolesklý kov', },
'Ca': { 'EN': 1.0, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 40.078, 'valency': (2,), 'ATOM_SYMBOL': u'Ca', 'NAME_LAT': u'calcium', 'OX_NUMBERS': [2], 'NAME_CZ': u'vápník', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 20, 'NAME_EN': u'calcium', 'DESC': u'měkký stříbrolesklý kov', },
'B': { 'EN': 2.04, 'group': 'non-metals',
'ATOM_WEIGHT': 10.811, 'valency': (3,), 'ATOM_SYMBOL': u'B', 'NAME_LAT': u'borium', 'OX_NUMBERS': [3], 'NAME_CZ': u'bor', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 5, 'NAME_EN': u'boron', 'DESC': u'pevná látka', },
'C': { 'EN': 2.55, 'group': 'non-metals',
'ATOM_WEIGHT': 12.0107, 'valency': (4, 2), 'ATOM_SYMBOL': u'C', 'NAME_LAT': u'carbonium', 'OX_NUMBERS': [4, 2, -4], 'NAME_CZ': u'uhlík', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 6, 'NAME_EN': u'carbon', 'DESC': u'měkký černý grafit, tvrdý bezbarvý diamant', },
'N': { 'EN': 3.04, 'group': 'non-metals',
'ATOM_WEIGHT': 14.0067, 'valency': (3, 5), 'ATOM_SYMBOL': u'N', 'NAME_LAT': u'nitrogenium', 'OX_NUMBERS': [5, 4, 3, 2, -3], 'NAME_CZ': u'dusík', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 7, 'NAME_EN': u'nitrogen', 'DESC': u'bezbarvý inertní plyn', },
'O': { 'EN': 3.44, 'group': 'non-metals',
'ATOM_WEIGHT': 15.9994, 'valency': (2,), 'ATOM_SYMBOL': u'O', 'NAME_LAT': u'oxygenium', 'OX_NUMBERS': [-2, -1], 'NAME_CZ': u'kyslík', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 8, 'NAME_EN': u'oxygen', 'DESC': u'reaktivní bezbarvý plyn', },
'F': { 'EN': 3.98, 'group': 'metals',
'ATOM_WEIGHT': 18.9984, 'valency': (1,), 'ATOM_SYMBOL': u'F', 'NAME_LAT': u'fluorum', 'OX_NUMBERS': [-1], 'NAME_CZ': u'fluor', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 9, 'NAME_EN': u'fluorine', 'DESC': u'reaktivní plyn', },
'Cl': { 'EN': 3.16, 'group': 'metals',
'ATOM_WEIGHT': 35.453, 'valency': (1, 3, 5, 7), 'ATOM_SYMBOL': u'Cl', 'NAME_LAT': u'chlorium', 'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'chlor', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 17, 'NAME_EN': u'chlorine', 'DESC': u'reaktivní žlutozelený plyn', },
'Br': { 'EN': 2.96, 'group': 'metals',
'ATOM_WEIGHT': 79.904, 'valency': (1, 3, 5), 'ATOM_SYMBOL': u'Br', 'NAME_LAT': u'bromium', 'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'brom', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 35, 'NAME_EN': u'bromine', 'DESC': u'reaktivní tmavě fialová kapalina', },
'I': { 'EN': 2.66, 'group': 'metals',
'ATOM_WEIGHT': 126.9045, 'valency': (1, 3, 5, 7), 'ATOM_SYMBOL': u'I', 'NAME_LAT': u'iodium', 'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'jod', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 53, 'NAME_EN': u'iodine', 'DESC': u'reaktivní tmavě fialová pevná látka', },
'Al': { 'EN': 1.61, 'group': 'other-metals',
'ATOM_WEIGHT': 26.9815, 'valency': (3,), 'ATOM_SYMBOL': u'Al', 'NAME_LAT': u'aluminium', 'OX_NUMBERS': [3], 'NAME_CZ': u'hliník', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 13, 'NAME_EN': u'aluminium', 'DESC': u'měkký stříbrošedý kov', },
'Si': { 'EN': 1.91, 'group': 'non-metals',
'ATOM_WEIGHT': 28.0855, 'valency': (4,), 'ATOM_SYMBOL': u'Si', 'NAME_LAT': u'silicium', 'OX_NUMBERS': [4, 2, -4], 'NAME_CZ': u'křemík', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 14, 'NAME_EN': u'silicon', 'DESC': u'šedý tvrdý a křehký polokov', },
'P': { 'EN': 2.19, 'group': 'non-metals',
'ATOM_WEIGHT': 30.9738, 'valency': (3, 5), 'ATOM_SYMBOL': u'P', 'NAME_LAT': u'phosphorus', 'OX_NUMBERS': [5, 3, -3], 'NAME_CZ': u'fosfor', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 15, 'NAME_EN': u'phosphorus', 'DESC': u'bílá, červená a černá modifikace', },
'S': { 'EN': 2.58, 'group': 'non-metals',
'ATOM_WEIGHT': 32.065, 'valency': (2, 4, 6), 'ATOM_SYMBOL': u'S', 'NAME_LAT': u'sulphurium', 'OX_NUMBERS': [6, 4, 2, -2], 'NAME_CZ': u'síra', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 16, 'NAME_EN': u'sulfur', 'DESC': u'žlutá krystalická látka', },
'Sn': { 'EN': 1.96, 'group': 'other-metals',
'ATOM_WEIGHT': 118.71, 'valency': (2, 4), 'ATOM_SYMBOL': u'Sn', 'NAME_LAT': u'stannum', 'OX_NUMBERS': [4, 2], 'NAME_CZ': u'cín', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 50, 'NAME_EN': u'tin', 'DESC': u'měkký stříbrolesklý kov', },
'As': { 'EN': 2.18, 'group': 'non-metals',
'ATOM_WEIGHT': 74.9216, 'valency': (3, 5), 'ATOM_SYMBOL': u'As', 'NAME_LAT': u'arsenicum', 'OX_NUMBERS': [5, 3, -3], 'NAME_CZ': u'arsen', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 33, 'NAME_EN': u'arsenic', 'DESC': u'lehký polokov', },
'Ne': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 20.1797, 'valency': (0, 2), 'ATOM_SYMBOL': u'Ne', 'NAME_LAT': u'neon', 'OX_NUMBERS': [], 'NAME_CZ': u'neon', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 10, 'NAME_EN': u'neon', 'DESC': u'bezbarvý inertní plyn', },
'Ar': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 39.948, 'valency': (0, 2), 'ATOM_SYMBOL': u'Ar', 'NAME_LAT': u'argon', 'OX_NUMBERS': [], 'NAME_CZ': u'argon', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 18, 'NAME_EN': u'argon', 'DESC': u'bezbarvý inertní plyn', },
'Pb': { 'EN': 2.33, 'group': 'other-metals',
'ATOM_WEIGHT': 207.2, 'valency': (2, 4), 'ATOM_SYMBOL': u'Pb', 'NAME_LAT': u'plumbum', 'OX_NUMBERS': [4, 2], 'NAME_CZ': u'olovo', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 82, 'NAME_EN': u'lead', 'DESC': u'měkký šedý kov', },
'Cr': { 'EN': 1.66, 'group': 'metals',
'ATOM_WEIGHT': 51.9961, 'valency': (2, 3, 6), 'ATOM_SYMBOL': u'Cr', 'NAME_LAT': u'chromium', 'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1, -2], 'NAME_CZ': u'chrom', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 24, 'NAME_EN': u'chromium', 'DESC': u'tvrdý stříbrolesklý kov', },
'Fe': { 'EN': 1.83, 'group': 'metals',
'ATOM_WEIGHT': 55.845, 'valency': (2, 3), 'ATOM_SYMBOL': u'Fe', 'NAME_LAT': u'ferrum', 'OX_NUMBERS': [6, 4, 5, 3, 2, 1, 0, -1, -2], 'NAME_CZ': u'železo', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 26, 'NAME_EN': u'iron', 'DESC': u'stříbrolesklý kov', },
'Zn': { 'EN': 1.65, 'group': 'metals',
'ATOM_WEIGHT': 65.39, 'valency': (2,), 'ATOM_SYMBOL': u'Zn', 'NAME_LAT': u'zincum', 'OX_NUMBERS': [2], 'NAME_CZ': u'zinek', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 30, 'NAME_EN': u'zinc', 'DESC': u'křehký modrobílý kov', },
'Ni': { 'EN': 1.91, 'group': 'metals',
'ATOM_WEIGHT': 58.6934, 'valency': (2, 3), 'ATOM_SYMBOL': u'Ni', 'NAME_LAT': u'niccolum', 'OX_NUMBERS': [4, 3, 2, 1, 0, -1], 'NAME_CZ': u'nikl', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 28, 'NAME_EN': u'nickel', 'DESC': u'bílý kov', },
'Au': { 'EN': 2.54, 'group': 'metals',
'ATOM_WEIGHT': 196.9665, 'valency': (1, 3), 'ATOM_SYMBOL': u'Au', 'NAME_LAT': u'aurum', 'OX_NUMBERS': [5, 3, 2, 1], 'NAME_CZ': u'zlato', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 79, 'NAME_EN': u'gold', 'DESC': u'měkký žlutý kov', },
'Ag': { 'EN': 1.93, 'group': 'metals',
'ATOM_WEIGHT': 107.8682, 'valency': (1,), 'ATOM_SYMBOL': u'Ag', 'NAME_LAT': u'argentum', 'OX_NUMBERS': [3, 2, 1], 'NAME_CZ': u'stříbro', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 47, 'NAME_EN': u'silver', 'DESC': u'měkký stříbrolesklý kov', },
'Pt': { 'EN': 2.28, 'group': 'metals',
'ATOM_WEIGHT': 195.078, 'valency': (2, 4), 'ATOM_SYMBOL': u'Pt', 'NAME_LAT': u'platinum', 'OX_NUMBERS': [6, 5, 4, 2, 0], 'NAME_CZ': u'platina', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 78, 'NAME_EN': u'platinum', 'DESC': u'stříbrolesklý kov', },
'Hg': { 'EN': 2.0, 'group': 'metals',
'ATOM_WEIGHT': 200.59, 'valency': (1, 2), 'ATOM_SYMBOL': u'Hg', 'NAME_LAT': u'hydrargyrum', 'OX_NUMBERS': [2, 1], 'NAME_CZ': u'rtuť', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 80, 'NAME_EN': u'mercury', 'DESC': u'stříbrolesklý kapalný kov', },
'Nb': { 'EN': 1.6, 'group': 'metals',
'ATOM_WEIGHT': 92.9064, 'valency': (3, 5), 'ATOM_SYMBOL': u'Nb', 'NAME_LAT': u'niobium', 'OX_NUMBERS': [5, 4, 3, 2, 1, -1], 'NAME_CZ': u'niob', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 41, 'NAME_EN': u'niobium', },
'Y': { 'EN': 1.22, 'group': 'metals',
'ATOM_WEIGHT': 88.9059, 'valency': (3,), 'ATOM_SYMBOL': u'Y', 'NAME_LAT': u'yttrium', 'OX_NUMBERS': [3], 'NAME_CZ': u'yttrium', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 39, 'NAME_EN': u'yttrium', },
'Tc': { 'EN': 1.9, 'group': 'metals',
'ATOM_WEIGHT': 98.9063, 'valency': (5, 7), 'ATOM_SYMBOL': u'Tc', 'NAME_LAT': u'technetium', 'OX_NUMBERS': [7, 6, 5, 4, 3, 2, 1, 0, -1, -3], 'NAME_CZ': u'technecium', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 43, 'NAME_EN': u'technetium', },
'Ta': { 'EN': 1.5, 'group': 'metals',
'ATOM_WEIGHT': 180.9479, 'valency': (5,), 'ATOM_SYMBOL': u'Ta', 'NAME_LAT': u'tantalum', 'OX_NUMBERS': [5, 4, 3, 2, 1, -1], 'NAME_CZ': u'tantal', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 73, 'NAME_EN': u'tantalum', },
'La': { 'EN': 1.1, 'group': 'metals',
'ATOM_WEIGHT': 138.9055, 'valency': (3,), 'ATOM_SYMBOL': u'La', 'NAME_LAT': u'lanthanum', 'OX_NUMBERS': [3], 'NAME_CZ': u'lanthan', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 57, 'NAME_EN': u'lanthanum', },
'Po': { 'EN': 2.0, 'group': 'other-metals',
'ATOM_WEIGHT': 208.9824, 'valency': (2, 4, 6), 'ATOM_SYMBOL': u'Po', 'NAME_LAT': u'polonium', 'OX_NUMBERS': [6, 4, 2], 'NAME_CZ': u'polonium', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 84, 'NAME_EN': u'polonium', },
'Hf': { 'EN': 1.3, 'group': 'metals',
'ATOM_WEIGHT': 178.49, 'valency': (4,), 'ATOM_SYMBOL': u'Hf', 'NAME_LAT': u'hafnium', 'OX_NUMBERS': [4, 3, 1], 'NAME_CZ': u'hafnium', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 72, 'NAME_EN': u'hafnium', },
'Sc': { 'EN': 1.36, 'group': 'metals',
'ATOM_WEIGHT': 44.9559, 'valency': (3, 1), 'ATOM_SYMBOL': u'Sc', 'NAME_LAT': u'scandium', 'OX_NUMBERS': [3], 'NAME_CZ': u'scandium', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 21, 'NAME_EN': u'scandium', },
'In': { 'EN': 1.78, 'group': 'other-metals',
'ATOM_WEIGHT': 114.818, 'valency': (3,), 'ATOM_SYMBOL': u'In', 'NAME_LAT': u'indium', 'OX_NUMBERS': [3, 2, 1], 'NAME_CZ': u'indium', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 49, 'NAME_EN': u'indium', },
'At': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 209.9871, 'valency': (1, 7), 'ATOM_SYMBOL': u'At', 'NAME_LAT': u'astatium', 'OX_NUMBERS': [7, 5, 3, 1, -1], 'NAME_CZ': u'astat', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 85, 'NAME_EN': u'astatine', },
'V': { 'EN': 1.63, 'group': 'metals',
'ATOM_WEIGHT': 50.9415, 'valency': (2, 4, 5), 'ATOM_SYMBOL': u'V', 'NAME_LAT': u'vanadium', 'OX_NUMBERS': [5, 4, 3, 2, 1, 0, -1, -3], 'NAME_CZ': u'vanad', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 23, 'NAME_EN': u'vanadium', 'DESC': u'tvrdý ocelově šedý kov', },
'Mn': { 'EN': 1.55, 'group': 'metals',
'ATOM_WEIGHT': 54.938, 'valency': (2, 3, 4, 6, 7), 'ATOM_SYMBOL': u'Mn', 'NAME_LAT': u'manganum', 'OX_NUMBERS': [7, 6, 5, 4, 3, 2, 1, 0, -1, -2, -3], 'NAME_CZ': u'mangan', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 25, 'NAME_EN': u'manganese', 'DESC': u'tvrdý a křehký stříbrolesklý kov', },
'Be': { 'EN': 1.57, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 9.0122, 'valency': (2,), 'ATOM_SYMBOL': u'Be', 'NAME_LAT': u'beryllium', 'OX_NUMBERS': [2], 'NAME_CZ': u'beryllium', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 4, 'NAME_EN': u'beryllium', 'DESC': u'lehký stříbrolesklý kov', },
'Sr': { 'EN': 0.95, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 87.62, 'valency': (2,), 'ATOM_SYMBOL': u'Sr', 'NAME_LAT': u'strontium', 'OX_NUMBERS': [2], 'NAME_CZ': u'stroncium', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 38, 'NAME_EN': u'strontium', 'DESC': u'stříbrolesklý kov', },
'Ba': { 'EN': 0.89, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 137.237, 'valency': (2,), 'ATOM_SYMBOL': u'Ba', 'NAME_LAT': u'barium', 'OX_NUMBERS': [2], 'NAME_CZ': u'barium', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 56, 'NAME_EN': u'barium', 'DESC': u'měkký stříbrolesklý kov', },
'Rb': { 'EN': 0.82, 'group': 'alkali-metals',
'ATOM_WEIGHT': 85.4678, 'valency': (1,), 'ATOM_SYMBOL': u'Rb', 'NAME_LAT': u'rubidium', 'OX_NUMBERS': [1], 'NAME_CZ': u'rubidium', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 37, 'NAME_EN': u'rubidium', 'DESC': u'reaktivní měkký a lehký stříbrolesklý kov', },
'Cs': { 'EN': 0.79, 'group': 'alkali-metals',
'ATOM_WEIGHT': 132.9055, 'valency': (1,), 'ATOM_SYMBOL': u'Cs', 'NAME_LAT': u'caesium', 'OX_NUMBERS': [1], 'NAME_CZ': u'cesium', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 55, 'NAME_EN': u'caesium', 'DESC': u'reaktivní měkký a lehký stříbrolesklý kov', },
'Mo': { 'EN': 2.16, 'group': 'metals',
'ATOM_WEIGHT': 95.94, 'valency': (3, 5, 6), 'ATOM_SYMBOL': u'Mo', 'NAME_LAT': u'molybdenum', 'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1, -2], 'NAME_CZ': u'molybden', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 42, 'NAME_EN': u'molybdenum', 'DESC': u'stříbrolesklý kov', },
'Ru': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 101.07, 'valency': (3, 4, 6, 8), 'ATOM_SYMBOL': u'Ru', 'NAME_LAT': u'ruthenium', 'OX_NUMBERS': [8, 7, 6, 5, 4, 3, 2, 1, 0, -2], 'NAME_CZ': u'ruthenium', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 44, 'NAME_EN': u'ruthenium', 'DESC': u'šedý a tvrdý ušlechtilý kov', },
'Rh': { 'EN': 2.28, 'group': 'metals',
'ATOM_WEIGHT': 102.9055, 'valency': (3, 4), 'ATOM_SYMBOL': u'Rh', 'NAME_LAT': u'rhodium', 'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1], 'NAME_CZ': u'rhodium', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 45, 'NAME_EN': u'rhodium', 'DESC': u'bezbarvý tažný kov', },
'Cd': { 'EN': 1.69, 'group': 'metals',
'ATOM_WEIGHT': 112.411, 'valency': (2,), 'ATOM_SYMBOL': u'Cd', 'NAME_LAT': u'cadmium', 'OX_NUMBERS': [2, 1], 'NAME_CZ': u'kadmium', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 48, 'NAME_EN': u'cadmium', 'DESC': u'bezbarvý tažný kov', },
'Pd': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 106.42, 'valency': (2, 4), 'ATOM_SYMBOL': u'Pd', 'NAME_LAT': u'palladium', 'OX_NUMBERS': [4, 3, 2, 0], 'NAME_CZ': u'palladium', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 46, 'NAME_EN': u'palladium', 'DESC': u'kujný a tažný stříbrolesklý kov', },
'Ga': { 'EN': 1.81, 'group': 'other-metals',
'ATOM_WEIGHT': 69.723, 'valency': (3,), 'ATOM_SYMBOL': u'Ga', 'NAME_LAT': u'gallium', 'OX_NUMBERS': [3, 2, 1], 'NAME_CZ': u'galium', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 31, 'NAME_EN': u'gallium', 'DESC': u'měkký stříbrolesklý kov', },
'Ge': { 'EN': 2.01, 'group': 'other-metals',
'ATOM_WEIGHT': 72.64, 'valency': (4,), 'ATOM_SYMBOL': u'Ge', 'NAME_LAT': u'germanium', 'OX_NUMBERS': [4, 2], 'NAME_CZ': u'germanium', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 32, 'NAME_EN': u'germanium', 'DESC': u'lesklý šedobílý polokov', },
'Se': { 'EN': 2.55, 'group': 'non-metals',
'ATOM_WEIGHT': 78.96, 'valency': (2, 4, 6), 'ATOM_SYMBOL': u'Se', 'NAME_LAT': u'selenium', 'OX_NUMBERS': [6, 4, -2], 'NAME_CZ': u'selen', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 34, 'NAME_EN': u'selenium', 'DESC': u'lesklý černošedý nekov', },
'Sb': { 'EN': 2.05, 'group': 'other-metals',
'ATOM_WEIGHT': 121.76, 'valency': (3, 5), 'ATOM_SYMBOL': u'Sb', 'NAME_LAT': u'stibium', 'OX_NUMBERS': [5, 3, -3], 'NAME_CZ': u'antimon', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 51, 'NAME_EN': u'antimony', 'DESC': u'stříbrolesklý křehký polokov', },
'Bi': { 'EN': 2.02, 'group': 'other-metals',
'ATOM_WEIGHT': 208.9804, 'valency': (3, 5), 'ATOM_SYMBOL': u'Bi', 'NAME_LAT': u'bisemutum', 'OX_NUMBERS': [5, 3], 'NAME_CZ': u'bismut', 'VAL_ELECTRONS': 5, 'PROTON_NUMBER': 83, 'NAME_EN': u'bismuth', 'DESC': u'lesklý narůžovělý kov', },
'Tl': { 'EN': 2.04, 'group': 'other-metals',
'ATOM_WEIGHT': 204.3833, 'valency': (1, 3), 'ATOM_SYMBOL': u'Tl', 'NAME_LAT': u'thallium', 'OX_NUMBERS': [3, 1], 'NAME_CZ': u'thallium', 'VAL_ELECTRONS': 3, 'PROTON_NUMBER': 81, 'NAME_EN': u'thallium', 'DESC': u'měkký šedý kov', },
'U': { 'EN': 1.38, 'group': 'rare-earth-metals',
'ATOM_WEIGHT': 238.0289, 'valency': (3, 4, 5, 6), 'ATOM_SYMBOL': u'U', 'NAME_LAT': u'uranium', 'OX_NUMBERS': [6, 5, 4, 3], 'NAME_CZ': u'uran', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 92, 'NAME_EN': u'uranium', 'DESC': u'těžký stříbrošedý radioaktivní kov', },
'Rn': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 222.0176, 'valency': (0, 2), 'ATOM_SYMBOL': u'Rn', 'NAME_LAT': u'radon', 'OX_NUMBERS': [2], 'NAME_CZ': u'radon', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 86, 'NAME_EN': u'radon', 'DESC': u'bezbarvý radioaktivní inertní plyn', },
'Re': { 'EN': 1.9, 'group': 'metals',
'ATOM_WEIGHT': 186.207, 'valency': (7,), 'ATOM_SYMBOL': u'Re', 'NAME_LAT': u'rhenium', 'OX_NUMBERS': [7, 6, 5, 4, 3, 2, 1, 0, -1, -3], 'NAME_CZ': u'rhenium', 'VAL_ELECTRONS': 7, 'PROTON_NUMBER': 75, 'NAME_EN': u'rhenium', 'DESC': u'měkký kujný kov', },
'Os': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 190.23, 'valency': (4, 6, 8), 'ATOM_SYMBOL': u'Os', 'NAME_LAT': u'osmium', 'OX_NUMBERS': [8, 6, 5, 4, 3, 2, 1, 0, -2], 'NAME_CZ': u'osmium', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 76, 'NAME_EN': u'osmium', 'DESC': u'modrošedý kov', },
'W': { 'EN': 2.36, 'group': 'metals',
'ATOM_WEIGHT': 183.84, 'valency': (6,), 'ATOM_SYMBOL': u'W', 'NAME_LAT': u'wolframium', 'OX_NUMBERS': [6, 5, 4, 3, 2, 0, -1, -2], 'NAME_CZ': u'wolfram', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 74, 'NAME_EN': u'tungsten', 'DESC': u'stříbrolesklý kov', },
'Co': { 'EN': 1.88, 'group': 'metals',
'ATOM_WEIGHT': 58.9332, 'valency': (2, 3), 'ATOM_SYMBOL': u'Co', 'NAME_LAT': u'cobaltum', 'OX_NUMBERS': [5, 4, 3, 2, 1, 0, -1], 'NAME_CZ': u'kobalt', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 27, 'NAME_EN': u'cobalt', 'DESC': u'tvrdý stříbrošedý kov', },
'Kr': { 'EN': 0.0, 'group': 'inert-gases',
'ATOM_WEIGHT': 83.8, 'valency': (0, 2), 'ATOM_SYMBOL': u'Kr', 'NAME_LAT': u'krypton', 'OX_NUMBERS': [2], 'NAME_CZ': u'krypton', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 36, 'NAME_EN': u'krypton', 'DESC': u'bezbarvý inertní plyn', },
'Ra': { 'EN': 0.9, 'group': 'alkali-earth-metals',
'ATOM_WEIGHT': 226.0254, 'valency': (2,), 'ATOM_SYMBOL': u'Ra', 'NAME_LAT': u'radium', 'OX_NUMBERS': [2], 'NAME_CZ': u'radium', 'VAL_ELECTRONS': 2, 'PROTON_NUMBER': 88, 'NAME_EN': u'radium', 'DESC': u'stříbrolesklý radioaktivní kov', },
'Li': { 'EN': 0.98, 'group': 'alkali-metals',
'ATOM_WEIGHT': 6.941, 'valency': (1,), 'ATOM_SYMBOL': u'Li', 'NAME_LAT': u'lithium', 'OX_NUMBERS': [1], 'NAME_CZ': u'lithium', 'VAL_ELECTRONS': 1, 'PROTON_NUMBER': 3, 'NAME_EN': u'lithium', 'DESC': u'měkký lehký stříbrolesklý kov', },
'Te': { 'EN': 2.1, 'group': 'non-metals',
'ATOM_WEIGHT': 127.6, 'valency': (2, 4, 6), 'ATOM_SYMBOL': u'Te', 'NAME_LAT': u'tellurium', 'OX_NUMBERS': [6, 4, 2, -2], 'NAME_CZ': u'tellur', 'VAL_ELECTRONS': 6, 'PROTON_NUMBER': 52, 'NAME_EN': u'tellurium', 'DESC': u'stříbrolesklý polokov', },
'Zr': { 'EN': 1.33, 'group': 'metals',
'ATOM_WEIGHT': 91.224, 'valency': (4,), 'ATOM_SYMBOL': u'Zr', 'NAME_LAT': u'zirconium', 'OX_NUMBERS': [4, 3, 2, 1], 'NAME_CZ': u'zirkon', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 40, 'NAME_EN': u'zirconium', 'DESC': u'látka stříbrošedý kov', },
'Ir': { 'EN': 2.2, 'group': 'metals',
'ATOM_WEIGHT': 192.217, 'valency': (3, 4, 6), 'ATOM_SYMBOL': u'Ir', 'NAME_LAT': u'iridium', 'OX_NUMBERS': [6, 5, 4, 3, 2, 1, 0, -1], 'NAME_CZ': u'iridium', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 77, 'NAME_EN': u'iridium', 'DESC': u'bílý tvrdý a křehký kov', },
'Ti': { 'EN': 1.54, 'group': 'metals',
'ATOM_WEIGHT': 47.867, 'valency': (4, 3), 'ATOM_SYMBOL': u'Ti', 'NAME_LAT': u'titanium', 'OX_NUMBERS': [4, 3, 2], 'NAME_CZ': u'titan', 'VAL_ELECTRONS': 4, 'PROTON_NUMBER': 22, 'NAME_EN': u'titanium', 'DESC': u'tvrdý a lehký stříbrolesklý kov', },
'Xe': { 'EN': 2.6, 'group': 'inert-gases',
'ATOM_WEIGHT': 131.293, 'valency': (0, 2), 'ATOM_SYMBOL': u'Xe', 'NAME_LAT': u'xenon', 'OX_NUMBERS': [2, 4, 6, 8], 'NAME_CZ': u'xenon', 'VAL_ELECTRONS': 8, 'PROTON_NUMBER': 54, 'NAME_EN': u'xenon', 'DESC': u'bezbarvý inertní plyn', },
}
