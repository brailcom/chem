/* Copyright (C) 2007, 2008 Brailcom, o.p.s.

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

var brailchem_mol_display_fragments = true;

function brailchem_molecule (smiles)
{
    var after_function = null;
    if (smiles)
        after_function = function () { brailchem_browse_on_start (this.document, smiles); };
    brailchem_switch_page ('chrome://brailchem/content/molecule.xul', 'molecule-textbox', after_function);
}

function brailchem_browse_on_start (document, smiles)
{
    document.getElementById ('molecule-textbox').setAttribute ('value', smiles);
    brailchem_display_smiles (document, smiles);
}

function brailchem_browse_smiles ()
{
    var smiles = document.getElementById ('molecule-textbox').value;
    brailchem_display_smiles (document, smiles);
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

function brailchem_display_smiles (document, smiles)
{
    brailchem_wait_start ();
    brailchem_mol_display_fragments = true;
    // Fetch data
    var data = brailchem_call_server ('smiles', smiles);
    if (data == null)
        return;
    // Remove old contents
    var top_box = document.getElementById ('molecule-display-inner-box');
    brailchem_remove_children (top_box);
    // Display data
    var top_element = data.documentElement;
    if (top_element.nodeName == 'inputerror')
        brailchem_display_error (top_element.childNodes[0].nodeValue);
    if (brailchem_elements_by_attribute (top_element, 'data', 'type', 'REACTION').length > 0)
        brailchem_display_reaction (top_element, document, top_box);
    else
        brailchem_display_molecule (top_element, document, top_box);
    brailchem_wait_end ();
}

function brailchem_display_reaction (element, document, top_box)
{
    var main_heading = document.getElementById ('brailchem-molecule-heading');
    brailchem_set_element_text (main_heading, brailchem_string ('brailchemMoleculeReaction', 'brailchem-molecule-strings'));
    var summary_box = brailchem_add_element (top_box, 'vbox', {class: 'brailchem-reaction-box'});
    var molecule_box = brailchem_add_element (top_box, 'vbox');
    var id_number = 1;
    function process_elements (type_name, label_name)
    {
        var items = brailchem_elements_by_attribute (element, 'data', 'type', type_name);
        if (items.length == 0)
            return;
        brailchem_add_element (molecule_box, 'separator');
        var summary_subbox = brailchem_add_element (summary_box, 'hbox');
        var molecule_subbox = brailchem_add_element (molecule_box, 'vbox');
        var label_string = brailchem_string (label_name, 'brailchem-molecule-strings');
        brailchem_add_element (summary_subbox, 'description', {}, label_string + ': ');
        brailchem_add_element (molecule_subbox, 'description', {class: 'header', level: 2}, label_string);
        var molecules = brailchem_elements_by_attribute (items[0], 'data', 'type', 'MOLECULE');
        for (var i = 0; i < molecules.length; i++) {
            var target_id = 'mol'+(id_number++);
            var name_node = brailchem_add_element (molecule_subbox, 'description', {id: target_id, class: 'header', level: 3});
            var name = brailchem_display_molecule (molecules[i], document, molecule_subbox, name_node, true);
            var attributes = {'brailchem-target': target_id, class: 'brailchem-reference'};
            brailchem_add_element (summary_subbox, 'description', attributes, name);
        }
    }
    process_elements ('REACTANTS', 'brailchemMoleculeReactants');
    process_elements ('REAGENTS', 'brailchemMoleculeReagents');
    process_elements ('PRODUCTS', 'brailchemMoleculeProducts');
    brailchem_focus (main_heading);
}

function brailchem_display_molecule (element, document, top_box, start_node, nofocus)
{
    var name_node = start_node || document.getElementById ('brailchem-molecule-heading');
    var references = [], labels = {};
    var name = '';
    var summary = brailchem_display_molecule_summary (element, top_box, name_node);
    if (summary) {
        var atoms = summary[0], fragments = summary[1];
        name = summary[2];
        brailchem_display_molecule_pieces (element, atoms, fragments, top_box, references, labels);
        if (! nofocus)
            brailchem_focus (name_node);
    }
    return name;
}

function brailchem_display_molecule_summary (element, top_box, name_node)
{
    var document = top_box.ownerDocument;
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
    brailchem_set_element_text (name_node, name);
    var grid = brailchem_add_element (top_box, 'grid');
    var rows = brailchem_add_element (grid, 'rows');
    for (var i in properties) {
        var property = properties[i];
        var row = brailchem_add_element (rows, 'row');
        brailchem_add_element (row, 'description', {value: property.name});
        brailchem_add_element (row, 'description', {}, property.value);
    }
    return [atoms, fragments, name];
}

function brailchem_display_molecule_pieces (document_element, atoms_element, fragments_element, box, references, labels)
{
    if (! atoms_element && ! fragments_element)
        return;
    var document = box.ownerDocument;
    // Prepare data
    var item_data = {};
    var item_numbers = {};
    var fragment_items = {};
    var items = document_element.getElementsByTagName ('data');
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        var item_type = item.getAttribute ('type');
        if (item_type != 'ATOM' && item_type != 'FRAGMENT')
            continue;
        var id = item.getAttribute ('id');
        var label = brailchem_mol_element_value (item.getElementsByTagName ('data')[0]);
        var number = (item_numbers[label] || 0) + 1;
        item_numbers[label] = number;
        var neighbors = [];
        item_data[id] = {id: id, label: label, number: number, neighbors: neighbors, in_fragment: false};
        var neighbor_elements = item.getElementsByTagName ('link');
        for (var j = 0; j < neighbor_elements.length; j++) {
            var link = neighbor_elements[j];
            var bond = link.getAttribute ('description');
            var target = link.getAttribute ('id');
            neighbors.push ({bond: bond, id: target});
        }
    }    
    var items = fragments_element.getElementsByTagName ('parts')[0].childNodes;
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        if (item.tagName != 'data')
            continue;
        var id = item.getAttribute ('id');
        var inner_atoms = item.getElementsByTagName ('data');
        for (var j = 0; j < inner_atoms.length; j++) {
            var candidate = inner_atoms[j];
            if (candidate.getAttribute ('type') == 'ATOM')
                fragment_items[inner_atoms[j].getAttribute ('id')] = id;
        }
        var inner_atoms = item.getElementsByTagName ('ref');
        for (var j = 0; j < inner_atoms.length; j++) {
            fragment_items[inner_atoms[j].getAttribute ('id')] = id;
        }
    }
    function process_items (element, list, separator)
    {
        var items = element.getElementsByTagName ('parts')[0].childNodes;
        for (var i = 0; i < items.length; i++) {
            var item = items[i];
            var tag = item.tagName;
            if (tag != 'data' && tag != 'ref')
                continue;
            var id = item.getAttribute ('id');
            list.push (id);
            item_data[id].separator = separator;
            if (fragment_items[id])
                item_data[id].in_fragment = true;
        }
    }
    var fragment_list = [];
    process_items (fragments_element, fragment_list, ' /');
    var atom_list = [];
    process_items (atoms_element, atom_list, '/');
    // Render data
    if (atom_list.length > 0 || fragment_list.length > 0) {
        var attached_elements_string = brailchem_string ('brailchemMoleculeAttachedElements', 'brailchem-molecule-strings');
        var heading = brailchem_string ('brailchemMoleculeParts', 'brailchem-molecule-strings');
        brailchem_add_element (box, 'description', {id: 'brailchem-heading', class: 'header', level: 4}, heading);
        function render_items (kind, list)
        {
            function add_reference (neighbor, hbox, is_exposed_fragment_item)
            {
                var neighbor_id = neighbor.id;
                var item_id = (((! is_exposed_fragment_item) && fragment_items[neighbor_id]) || neighbor_id);                
                var neighbor_data = item_data[item_id];
                var label = neighbor_data.label + neighbor_data.separator + neighbor_data.number + '[' + neighbor.bond + ']';
                var attributes = {'brailchem-target': neighbor_data.id,
                                  value: label,
                                  'class': 'brailchem-reference',
                                  onfocus: 'brailchem_mol_atom_focus(this.parentNode.parentNode)'};
                if (neighbor_id != item_id)
                    attributes['brailchem-ghost-akin'] = 'fragment';
                brailchem_add_element (hbox, 'brailchemreference', attributes);
                if (neighbor_id != item_id) {
                    neighbor_data = item_data[neighbor_id];
                    attributes['brailchem-target'] = neighbor_data.id;
                    attributes['value'] = neighbor_data.label + neighbor_data.separator + neighbor_data.number + '[' + neighbor.bond + ']';
                    attributes['brailchem-ghost-akin'] = 'atom';
                    attributes['hidden'] = 'true';
                    brailchem_add_element (hbox, 'brailchemreference', attributes);
                }                
            }
            var box_class = 'brailchem-' + kind + '-box';
            var item_class = 'brailchem-' + kind;
            var box_hidden = (! brailchem_mol_display_fragments && kind == 'fragment' ? 'true' : 'false');
            for (var i in list) {
                var item_box = brailchem_add_element (box, 'vbox', {class: box_class, hidden: box_hidden});
                if (kind == 'fragment')
                    item_box.setAttribute ('brailchem-ghost-akin', kind);
                var id = list[i];
                var item = item_data[id];
                var is_exposed_fragment_item = (item.in_fragment && kind == 'atom');
                if (is_exposed_fragment_item) {
                    item_box.setAttribute ('brailchem-ghost-akin', kind);
                    item_box.setAttribute ('hidden', 'true');
                }
                var label = item.label + item.separator + item.number;
                var neighbors = item.neighbors;
                var hbox = brailchem_add_element (item_box, 'hbox');
                brailchem_add_element (hbox, 'description',
                                       {id: id, class: item_class, onfocus: 'brailchem_mol_atom_focus(this.parentNode.parentNode)'},
                                       label);
                var terminals = [];
                var nonterminals = [];
                for (var j in neighbors) {
                    var neighbor = neighbors[j];
                    if (fragment_items[neighbor.id] != id)
                        (item_data[neighbor.id].neighbors.length > 1 ? nonterminals : terminals).push (neighbor);
                }
                if (terminals.length > 0) {
                    brailchem_add_element (hbox, 'description', {}, attached_elements_string);
                    for (var j in terminals)
                        add_reference (terminals[j], hbox, is_exposed_fragment_item);
                }
                var hbox = brailchem_add_element (item_box, 'hbox');
                brailchem_add_element (hbox, 'description', {}, "Neighbors:");
                for (var j in nonterminals)
                    add_reference (nonterminals[j], hbox, is_exposed_fragment_item);
            }
        }
        render_items ('fragment', fragment_list);
        render_items ('atom', atom_list);
        // Fragment display switch
        if (fragment_list.length > 0)
            brailchem_add_element (box, 'checkbox', {id: 'brailchem-mol-fragment-switch', label: "Display atom groups",
                                                     checked: brailchem_mol_display_fragments,
                                                     oncommand: 'brailchem_mol_toggle_fragments(this)'});
    }
}

// Callbacks

function brailchem_mol_atom_focus (element)
{
    var atoms = document.getElementsByAttribute ('brailchem-current', 'true');
    for (var i = 0; i < atoms.length; i++)
        atoms[i].setAttribute ('brailchem-current', 'false');
    element.setAttribute ('brailchem-current', 'true');
}

function brailchem_mol_toggle_fragments (element)
{
    brailchem_mol_display_fragments = ! brailchem_mol_display_fragments;
    var hiding_akin = (brailchem_mol_display_fragments ? 'atom' : 'fragment');
    var showing_akin = (brailchem_mol_display_fragments ? 'fragment' : 'atom'); 
    var to_hide = document.getElementsByAttribute ('brailchem-ghost-akin', hiding_akin);
    for (var i = 0; i < to_hide.length; i++)
        to_hide[i].setAttribute ('hidden', 'true');
    var to_show = document.getElementsByAttribute ('brailchem-ghost-akin', showing_akin);
    for (var i = 0; i < to_show.length; i++)
        to_show[i].setAttribute ('hidden', '0');
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
