/* Copyright (C) 2007 Brailcom, o.p.s.

   COPYRIGHT NOTICE

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

function brailchem_molecule ()
{
    brailchem_switch_page ('chrome://brailchem/content/molecule.xul');
}

function brailchem_browse_molecule ()
{
    var smiles = document.getElementById ('molecule-textbox').value;
    brailchem_display_molecule (smiles);
}

function brailchem_mol_element_text (element) {
    var text = element.childNodes[0].nodeValue;
    for (var i = 0; i < text.length; i++) {
        ch = text.charAt (i);
        if (ch != ' ' && ch != '\n')
            break;
    }
    if (i > 0)
        text = text.substring (i);
    for (var i = text.length; i > 0; i--) {
        ch = text.charAt (i-1);
        if (ch != ' ' && ch != '\n')
            break;
    }
    if (i < text.length)
        text = text.substring (0, i);
    return text;
}

function brailchem_mol_element_value (element)
{
    var children = element.childNodes;
    for (var i = 0; i < children.length; i++) {
        if (children[i].nodeName == 'value')
            return brailchem_mol_element_text (children[i]);
    }
    return null;
}

function brailchem_display_molecule (smiles)
{
    brailchem_wait_start ();
    // Fetch data
    var doc = brailchem_call_server ('smiles', smiles);
    if (doc == null)
        return;
    // Remove old contents
    var top_box = document.getElementById ('molecule-display-inner-box');
    brailchem_remove_children (top_box);
    // Display data
    var element = doc.documentElement;
    if (element.nodeName == 'inputerror')
        brailchem_display_error (element.childNodes[0].nodeValue);
    else {
        var references = [], labels = {};
        var summary = brailchem_display_molecule_summary (element, top_box);
        if (summary) {
            var atoms = summary[0], fragments = summary[1];
            brailchem_display_pieces (atoms, fragments, top_box, references, labels);
            var name_node = document.getElementById ('brailchem-molecule-heading');
            brailchem_focus (name_node);
        }
    }
    brailchem_wait_end ();
}

function brailchem_display_molecule_summary (element, top_box)
{
    var molecule_element = element;
    var name = "Unknown molecule";
    var properties = [];
    var atoms = null;
    var fragments = null;
    var children = element.getElementsByTagName ('views')[0].childNodes;
    for (var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.tagName != 'data')
            continue;
        var type = child.getAttribute ('type');
        if (type == 'FRAGMENTS')
            fragments = child;
        else if (type == 'ATOMS')
            atoms = child;
        else {
            var property_name = child.getAttribute ('description');
            var property_value = brailchem_mol_element_value (child);
            properties.push ({name: property_name, value: property_value});
            if (type == 'NAME')
                name = property_value;
        }
    }
    var name_node = document.getElementById ('brailchem-molecule-heading');
    brailchem_set_element_text (name_node, name);
    var grid = brailchem_add_element (top_box, 'grid');
    var rows = brailchem_add_element (grid, 'rows');
    for (var i in properties) {
        var property = properties[i];
        var row = brailchem_add_element (rows, 'row');
        brailchem_add_element (row, 'description', {value: property.name});
        brailchem_add_element (row, 'description', {}, property.value);
    }
    return [atoms, fragments];
}

function brailchem_display_pieces (atoms_element, fragments_element, box, references, labels)
{
    if (! atoms_element)
        return;
    var atom_data = {};
    var atom_list = [];
    var atom_numbers = {};
    var atoms = atoms_element.getElementsByTagName ('parts')[0].childNodes;
    for (var i = 0; i < atoms.length; i++) {
        var atom = atoms[i];
        if (atom.tagName != 'data')
            continue;
        var id = atom.getAttribute ('id');
        var label = brailchem_mol_element_value (atom.getElementsByTagName ('data')[0]);
        var number = (atom_numbers[label] || 0) + 1;
        atom_numbers[label] = number;
        var neighbors = [];
        atom_data[id] = {id: id, label: label, number: number, neighbors: neighbors};
        atom_list.push (id);
        var neighbor_elements = atom.getElementsByTagName ('link');
        for (var j = 0; j < neighbor_elements.length; j++) {
            var link = neighbor_elements[j];
            var bond = link.getAttribute ('description');
            var target = link.getAttribute ('id');
            neighbors.push ({bond: bond, id: target});
        }
    }
    if (atoms.length > 0) {
        brailchem_add_element (box, 'description', {id: 'brailchem-atom-heading', class: 'header', level: 2}, "Atoms");
        for (var i in atom_list) {
            var atom_box = brailchem_add_element (box, 'vbox', {class: 'brailchem-atom-box', onfocus: 'brailchem_mol_atom_focus(this)'});
            var id = atom_list[i];
            var atom = atom_data[id];
            var label = atom.label+'/'+atom.number;
            var neighbors = atom.neighbors;
            var hbox = brailchem_add_element (atom_box, 'hbox');
            brailchem_add_element (hbox, 'description', {id: id, class: 'brailchem-atom'}, label);
            var terminals = [];
            var nonterminals = [];
            for (var j in neighbors) {
                neighbor = neighbors[j];
                (atom_data[neighbor.id].neighbors.length > 1 ? nonterminals : terminals).push (neighbor);
            }
            function add_reference (neighbor)
            {
                var neighbor_data = atom_data[neighbor.id];
                var label = neighbor_data.label + '/' + neighbor_data.number + '[' + neighbor.bond + ']';
                brailchem_add_element (hbox, 'brailchemreference', {'brailchem-target': neighbor.id, value: label, class: 'brailchem-reference'});
            }
            if (terminals.length > 0) {
                brailchem_add_element (hbox, 'description', {}, "Attached elements:");
                for (var j in terminals)
                    add_reference (terminals[j]);
            }
            var hbox = brailchem_add_element (atom_box, 'hbox');
            brailchem_add_element (hbox, 'description', {}, "Neighbors:");
            for (var j in nonterminals)
                add_reference (nonterminals[j]);
        }
    }
}

// Callbacks

function brailchem_mol_atom_focus (element)
{
    var atoms = document.getElementsByAttribute ('brailchem-current', 'true');
    for (var i = 0; i < atoms.length; i++)
        atoms[i].setAttribute ('brailchem-current', 'false');
    //element.parentNode.parentNode.setAttribute ('brailchem-current', 'true');
    element.setAttribute ('brailchem-current', 'true');
}

// Commands

function brailchem_mol_go_atoms ()
{
    brailchem_focus (document.getElementById ('brailchem-atom-heading'), true);
}

function brailchem_mol_move_atom (forward)
{
    var atoms = document.getElementsByAttribute ('class', 'brailchem-atom-box');
    var index = null;
    for (var i = 0; i < atoms.length; i++)
        if (atoms[i].getAttribute ('brailchem-current') == 'true') {
            index = i + (forward ? 1 : -1);
            break;
        }
    if (index == null)
        index = (forward ? 0 : atoms.length - 1);
    if (index < 0) {
        brailchem_message ("No previous atom");
        return;
    }
    if (index >= atoms.length) {
        brailchem_message ("No next atom");
        return;
    }
    brailchem_focus (atoms[index], true);
}

function brailchem_mol_next_atom ()
{
    brailchem_mol_move_atom (true);
}

function brailchem_mol_previous_atom ()
{
    brailchem_mol_move_atom (false);
}

function brailchem_follow_reference (element)
{
    var id = element.getAttribute ('brailchem-target');
    var target = document.getElementById (id);
    brailchem_focus (target);
}
