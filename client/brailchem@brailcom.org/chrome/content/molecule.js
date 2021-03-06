/* Copyright (C) 2007, 2008, 2009 Brailcom, o.p.s.

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
var brailchem_mol_last_reaction_element = true;
var brailchem_mol_highlighted_image_elements = [];
var brailchem_mol_fragment_atoms = {};

function brailchem_molecule (value, format)
{
    var after_function = function () { brailchem_molecule_formats (this); }
    if (format)
        after_function = function () { brailchem_molecule_formats (this);
                                       brailchem_browse_on_start (this.document, value, format); };
    brailchem_switch_page ('chrome://brailchem/content/molecule.xul', 'molecule-textbox', after_function);
}

function brailchem_molecule_formats (page)
{
    var data = brailchem_call_server ('formats');
    if (data == null)
        return;
    var menu = page.find_element ('molecule-format-menu');
    var formats = data.getElementsByTagName ('format');
    for (var i = 0; i < formats.length; i++) {
        var format = formats[i];
        if (format.getAttribute ('common')) {
            var name = brailchem_mol_element_text (format.getElementsByTagName ('name')[0]);
            var description = brailchem_mol_element_text (format.getElementsByTagName ('description')[0]);
            // XUL, oh, XUL, ...  It's not possible to store data about file
            // extensions to a global variable, because its in some different
            // scope during initialization.  Attributes fortunately survive...
            var extension_string = format.getAttribute ('extensions');
            if (extension_string) {
                extension_string = extension_string + ' ';
                var extension_list = '';
                while (extension_string) {
                    var space_index = extension_string.indexOf (' ');
                    var extension = extension_string.substring (0, space_index);
                    extension_list = extension_list + '[' + extension + ']';
                    extension_string = extension_string.substring (space_index + 1);
                }
            }
            else
                extension_list = '';
            attributes = {value: name, label: description, 'brailchem-extensions': extension_list};
            brailchem_add_element (menu, 'menuitem', attributes);
        }
    }
    page.find_element ('molecule-format').selectedIndex = 0;
}

function brailchem_browse_on_start (document, value, format)
{
    document.getElementById ('molecule-textbox').setAttribute ('value', value);
    // We try to set the format in the format combo box.
    // It doesn't work, but it remains here for reference.
    var menu = document.getElementById ('molecule-format-menu');
    var selected_nodes = menu.getElementsByAttribute ('selected', 'true');
    for (var i = 0; i < selected_nodes.length; i++)
        selected_nodes[i].setAttribute ('selected', 'false');
    var menu_item = menu.getElementsByAttribute ('value', format)[0];
    if (menu_item)
        menu_item.setAttribute ('selected', 'true');
    brailchem_display_object (document, value, format);
}

function brailchem_is_url (molecule_or_uri)
{
    var prefix = molecule_or_uri.substring (0, 5);
    return (prefix == 'file:' || prefix == 'http:');
}

function brailchem_browse_molecule ()
{
    var format = document.getElementById ('molecule-format').value;
    var molecule_or_uri = document.getElementById ('molecule-textbox').value;
    var molecule = (brailchem_is_url (molecule_or_uri) ? brailchem_read_url (molecule_or_uri) : molecule_or_uri);
    brailchem_display_object (document, molecule, format);
}

function brailchem_browse_name ()
{
    var name = document.getElementById ('molecule-textbox').value;
    brailchem_display_object (document, name, 'name');
}

function brailchem_mol_insert_file ()
{
    var file = brailchem_select_file ();
    if (! file)
        return;
    var url = 'file:' + file.path;
    var input_field = document.getElementById ('molecule-textbox');
    input_field.value = url;
    brailchem_mol_set_format (input_field);
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

function brailchem_display_object (document, input_value, format)
{
    brailchem_wait_start ();
    brailchem_mol_display_fragments = true;
    brailchem_mol_last_reaction_element = null;
    brailchem_mol_fragment_atoms = {};
    // Fetch data
    var data = brailchem_call_server ('chemfile', [{name: 'format', value: format},
                                                   {name: 'uploaded_file', value: input_value}]);
    if (data == null)
        return;
    // Remove old contents
    var top_box = document.getElementById ('molecule-display-inner-box');
    brailchem_remove_children (top_box);
    // Display data
    var top_element = data.documentElement;
    if (top_element.nodeName == 'inputerror')
        brailchem_display_error (top_element.childNodes[0].nodeValue);
    else {
        var fragment_checkbox = document.getElementById ('brailchem-mol-fragment-switch');
        fragment_checkbox.setAttribute ('hidden', 'true');
        fragment_checkbox.setAttribute ('checked', brailchem_mol_display_fragments);
        if (brailchem_elements_by_attribute (top_element, 'data', 'type', 'REACTION').length > 0)
            brailchem_display_reaction (top_element, document, top_box);
        else
            brailchem_display_molecule (top_element, document, top_box);
    }
    brailchem_wait_end ();
}

function brailchem_display_reaction (element, document, top_box)
{
    var main_heading = document.getElementById ('brailchem-molecule-heading');
    brailchem_set_element_text (main_heading, brailchem_string ('brailchemMoleculeReaction', 'brailchem-molecule-strings'));
    brailchem_mol_last_reaction_element = main_heading;
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
            var name_node = brailchem_add_element (molecule_subbox, 'description',
                                                   {id: target_id, 'brailchem-mol-id': target_id, 'brailchem-mol-name': true,
                                                    class: 'header', level: 3, 'brailchem-current': 'false',
                                                    onfocus: 'brailchem_mol_atom_focus(this,'+target_id+')'});
            var name = brailchem_display_molecule (molecules[i], document, molecule_subbox, name_node, target_id);
            var attributes = {'brailchem-target': target_id, class: 'brailchem-reference', value: 'go '+name,
                              onfocus: 'brailchem_mol_last_reaction_element=this'};
            brailchem_add_element (summary_subbox, 'brailchemreference', attributes);
        }
    }
    process_elements ('REACTANTS', 'brailchemMoleculeReactants');
    process_elements ('REAGENTS', 'brailchemMoleculeReagents');
    process_elements ('PRODUCTS', 'brailchemMoleculeProducts');
    brailchem_focus (main_heading);
}

function brailchem_display_molecule (element, document, top_box, start_node, mol_id)
{
    var name_node = start_node || document.getElementById ('brailchem-molecule-heading');
    var references = [], labels = {};
    var name = '';
    var summary = brailchem_display_molecule_summary (element, top_box, name_node);
    if (summary) {
        var atoms = summary[0], fragments = summary[1], name = summary[2], image = summary[3];
        brailchem_display_molecule_pieces (element, atoms, fragments, top_box, references, labels, mol_id);
        if (! mol_id)
            brailchem_focus (name_node);
        brailchem_display_molecule_image (document, image);
    }
    return name;
}

function brailchem_display_molecule_summary (element, top_box, name_node)
{
    var document = top_box.ownerDocument;
    var molecule_element = element;
    var name = brailchem_string ('brailchemMoleculeUnknown', 'brailchem-molecule-strings');
    var properties = [];
    var atoms = null;
    var fragments = null;
    var views = element.getElementsByTagName ('views')[0];
    if (! views) {
        brailchem_alert (brailchem_string ('brailchemEmptyResponse', 'brailchem-strings'));
        return null;
    }
    var children = views.childNodes;
    var image = null;
    for (var i = 0; i < children.length; i++) {
        var child = children[i];
        if (child.tagName != 'data')
            continue;
        var type = child.getAttribute ('type');
        if (type == 'FRAGMENTS')
            fragments = child;
        else if (type == 'ATOMS')
            atoms = child;
        else if (child.getAttribute ('type') == 'MOL_PICTURE') {
            var xml_image = brailchem_mol_element_value (child);
            var parser = new DOMParser();
            image = parser.parseFromString (xml_image, "text/xml");
        }
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
    return [atoms, fragments, name, image];
}

function brailchem_display_molecule_pieces (document_element, atoms_element, fragments_element, box, references, labels, mol_id)
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
        var node_data = item.getElementsByTagName ('data');
        var label = '';
        var charge = '0';
        var multiplicity = '1';
        var part_of_rings = 0;
        var stereochemistry = null;
        for (var j = 0; j < node_data.length; j++) {
            var node_data_j = node_data[j];
            var node_data_type = node_data_j.getAttribute ('type');
            if (node_data_type == 'FRAGMENT_NAME' || (node_data_type == 'ATOM_SYMBOL' && label == ''))
                label = brailchem_mol_element_value (node_data_j);
            else if (node_data_type == 'ATOM_CHARGE')
                charge = brailchem_mol_element_value (node_data_j);
            else if (node_data_type == 'ATOM_MULTIPLICITY')
                multiplicity = brailchem_mol_element_value (node_data_j);
            else if (node_data_type == 'PART_OF_RINGS')
                part_of_rings = 0 + brailchem_mol_element_value (node_data_j);
            else if (node_data_type == 'STEREOCHEMISTRY')
                stereochemistry = brailchem_mol_element_value (node_data_j);
        }
        if (charge != '0') {
            var charge_label = (charge == '1' ? '+' :
                                charge == '-1' ? '-' :
                                charge > 0 ? '+' + charge :
                                charge);
            label = label + charge_label;
        }
        var number = (item_numbers[label] || 0) + 1;
        item_numbers[label] = number;
        var neighbors = [];
        item_data[id] = {id: id, label: label, number: number, neighbors: neighbors, in_fragment: null,
                         multiplicity: multiplicity, part_of_rings: part_of_rings,
                         stereochemistry: stereochemistry};
        var neighbor_elements = item.getElementsByTagName ('link');
        var neighbors_length = 0;
        for (var j = 0; j < neighbor_elements.length; j++) {
            var link = neighbor_elements[j];
            var link_type = link.getAttribute ('type');
            if (link_type.indexOf ('BOND') != -1)
                neighbors_length++;
            var bond = link.getAttribute ('description');
            var target = link.getAttribute ('id');
            var aromatic = link.getAttribute ('aromatic') == '1';
            neighbors.push ({bond: bond, id: target, aromatic: aromatic});
        }
        item_data[id].neighbors_length = neighbors_length;
    }    
    var items = fragments_element.getElementsByTagName ('parts')[0].childNodes;
    for (var i = 0; i < items.length; i++) {
        var item = items[i];
        if (item.tagName != 'data')
            continue;
        var id = item.getAttribute ('id');
        brailchem_mol_fragment_atoms[id] = [];
        var inner_atoms = item.getElementsByTagName ('data');
        for (var j = 0; j < inner_atoms.length; j++) {
            var candidate = inner_atoms[j];
            if (candidate.getAttribute ('type') == 'ATOM') {
                var atom_id = candidate.getAttribute ('id');
                fragment_items[atom_id] = id;
                brailchem_mol_fragment_atoms[id].push (atom_id);
            }
        }
        var inner_atoms = item.getElementsByTagName ('ref');
        for (var j = 0; j < inner_atoms.length; j++) {
            var atom_id = inner_atoms[j].getAttribute ('id');
            fragment_items[atom_id] = id;
            brailchem_mol_fragment_atoms[id].push (atom_id);            
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
            var fragment_id = fragment_items[id];
            if (fragment_id)
                item_data[id].in_fragment = fragment_id;
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
            function add_reference (neighbor, hbox, is_exposed_fragment_item, image_element_id)
            {
                var neighbor_id = neighbor.id;
                var item_id = (((! is_exposed_fragment_item) && fragment_items[neighbor_id]) || neighbor_id);                
                var neighbor_data = item_data[item_id];
                var bond_description = '[' + neighbor.bond + (neighbor.aromatic ? ' A' : '') + ']';
                var label = neighbor_data.label + neighbor_data.separator + neighbor_data.number + bond_description;
                var attributes = {'brailchem-target': neighbor_data.id,
                                  value: label,
                                  'class': 'brailchem-reference',
                                  onfocus: 'brailchem_mol_atom_focus(this.parentNode.parentNode, '+image_element_id+')'};
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
            function sort_atoms (id1, id2)
            {
                var n1 = item_data[id1].neighbors_length;
                var n2 = item_data[id2].neighbors_length;
                if (n1 > n2)
                    return -1;
                if (n1 < n2)
                    return 1;
                if (id1 < id2)
                    return -1;
                if (id1 > id2)
                    return 1;
                return 0;
            }
            // Sorting atoms disabled to make stereochemistry work
            // list.sort (sort_atoms);
            for (var i in list) {
                var item_box = brailchem_add_element (box, 'vbox', {class: box_class, hidden: box_hidden,
                                                                    'brailchem-atom-or-fragment': true, 'brailchem-mol-id': mol_id});
                if (kind == 'fragment')
                    item_box.setAttribute ('brailchem-ghost-akin', kind);
                var id = list[i];
                var item = item_data[id];
                var is_exposed_fragment_item = (item.in_fragment != null && kind == 'atom');
                if (is_exposed_fragment_item) {
                    item_box.setAttribute ('brailchem-ghost-akin', kind);
                    item_box.setAttribute ('hidden', 'true');
                }
                var label = item.label + item.separator + item.number;
                var neighbors = item.neighbors;
                var hbox = brailchem_add_element (item_box, 'hbox');
                brailchem_add_element (hbox, 'description',
                                       {id: id, class: item_class, 'brailchem-fragment': (item.in_fragment || ''),
                                        onfocus: 'brailchem_mol_atom_focus(this.parentNode.parentNode,'+id+')'},
                                       label);
                if (item.part_of_rings > 0) {
                    var part_of_rings_label = ' ';
                    for (var i = 0; i < item.part_of_rings; i++)
                        part_of_rings_label = part_of_rings_label + 'R';
                    brailchem_add_element (hbox, 'description', {}, part_of_rings_label);
                }
                if (item.multiplicity && item.multiplicity != '1')
                    brailchem_add_element (hbox, 'description', {}, ' x'+item.multiplicity);
                if (item.stereochemistry)
                    brailchem_add_element (hbox, 'description', {}, 'STEREO:'+item.stereochemistry);
                var terminals = [];
                var nonterminals = [];
                var number_of_neighbors = 0;
                for (var j in neighbors) {
                    var neighbor = neighbors[j];
                    if (fragment_items[neighbor.id] != id) {
                        number_of_neighbors++;
                        // Stereochemistry requires not to split the list
                        nonterminals.push (neighbor);
                    }
                }
                var hbox = brailchem_add_element (item_box, 'hbox');
                var neighbors_string = (number_of_neighbors == 1 ? 'brailchemMoleculeNeighbor1' :
                                        number_of_neighbors == 2 ? 'brailchemMoleculeNeighbor2' :
                                        number_of_neighbors == 3 ? 'brailchemMoleculeNeighbor3' :
                                        number_of_neighbors == 4 ? 'brailchemMoleculeNeighbor4' :
                                        'brailchemMoleculeNeighbors');
                var neighbors_label = number_of_neighbors + ' ' + brailchem_string (neighbors_string, 'brailchem-molecule-strings');
                var hbox = brailchem_add_element (item_box, 'hbox');
                var box_element_attributes = {onfocus: 'brailchem_highlight_molecule_image('+id+')'};
                brailchem_add_element (hbox, 'description', box_element_attributes, neighbors_label);
                for (var j in nonterminals)
                    add_reference (nonterminals[j], hbox, is_exposed_fragment_item, id);
                if (terminals.length > 0) {
                    brailchem_add_element (hbox, 'description', box_element_attributes, ' * ');
                    for (var j in terminals)
                        add_reference (terminals[j], hbox, is_exposed_fragment_item, id);
                }                
            }
        }
        render_items ('fragment', fragment_list);
        render_items ('atom', atom_list);
        // Fragment display switch
        if (fragment_list.length > 0)
            document.getElementById ('brailchem-mol-fragment-switch').setAttribute ('hidden', 'false');
    }
}

function brailchem_display_molecule_image (document, image)
{
    var image_box = document.getElementById ('brailchem-molecule-image-box');
    var image_node = document.getElementById ('brailchem-molecule-image');
    var image_element = image.documentElement;
    image_element.setAttribute ('id', 'brailchem-molecule-image');
    image_box.replaceChild (image_element, image_node);
    brailchem_mol_highlighted_image_elements = [];
}

function brailchem_highlight_molecule_image (id)
{
    if (! id)
        return;
    highlighted = [];
    function highlight (id)
    {
        var element_to_highlight = document.getElementById ('h-'+id);
        if (element_to_highlight) {
            element_to_highlight.setAttribute ('stroke', '#800');
            element_to_highlight.setAttribute ('stroke-opacity', 1);
            element_to_highlight.setAttribute ('fill-opacity', 0.5);
            highlighted.push (element_to_highlight);
        }
    }
    atoms = brailchem_mol_fragment_atoms[id];
    if (atoms)
        for (var i = 0; i < atoms.length; i++)
            highlight (atoms[i]);
    else
        highlight (id);
    for (var i = 0; i < brailchem_mol_highlighted_image_elements.length; i++) {
        var element_to_unhighlight = brailchem_mol_highlighted_image_elements[i];
        if (highlighted.indexOf (element_to_unhighlight) == -1) {
            element_to_unhighlight.setAttribute ('stroke-opacity', 0);
            element_to_unhighlight.setAttribute ('fill-opacity', 0);
        }
    }
    brailchem_mol_highlighted_image_elements = highlighted;
}

function brailchem_mol_focus (element)
{
    brailchem_highlight_molecule_image (element.id);
    brailchem_focus (element);
}

// Callbacks

function brailchem_mol_atom_focus (element, image_element_id)
{
    var atoms = document.getElementsByAttribute ('brailchem-current', 'true');
    for (var i = 0; i < atoms.length; i++)
        atoms[i].setAttribute ('brailchem-current', 'false');
    element.setAttribute ('brailchem-current', 'true');
    if (image_element_id)
        brailchem_highlight_molecule_image (image_element_id);
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

function brailchem_mol_set_format (element)
{
    var value = element.value;
    if (! brailchem_is_url (value))
        return;
    var extension_index = value.lastIndexOf ('.');
    if (extension_index == -1)
        return;
    var extension = '[' + value.substring (extension_index + 1) + ']';
    var menu_items = document.getElementById ('molecule-format-menu').getElementsByTagName ('menuitem');
    for (var i = 0; i < menu_items.length; i++) {
        var extension_list = menu_items[i].getAttribute ('brailchem-extensions');
        if (extension_list.indexOf (extension) > -1) {
            document.getElementById('molecule-format').selectedIndex = i;
            break;
        }
    }
}

// Commands

function brailchem_mol_go_atoms ()
{
    brailchem_mol_move_object (null, 'atoms');
}

function brailchem_mol_move_object (forward, kind)
{
    brailchem_clear_message ();
    var first_move = false;
    var current_list = document.getElementsByAttribute ('brailchem-current', 'true');
    if (current_list.length == 0) {
        current_list = document.getElementsByAttribute ('brailchem-atom-or-fragment', 'true');
        first_move = true;
    }
    var current = current_list[0];
    var current_class = current.getAttribute ('class');
    var current_is_atom = (current_class == 'brailchem-atom-box' || current_class == 'brailchem-fragment-box');
    var mol_id = current.getAttribute ('brailchem-mol-id');
    if (kind == 'atoms') {
        var atoms = document.getElementsByAttribute ('brailchem-mol-id', mol_id);
        var elements = [];
        for (var i = 0; i < atoms.length; i++) {
            var element_class = atoms[i].getAttribute ('class');
            if ((element_class == 'brailchem-atom-box' || element_class == 'brailchem-fragment-box') &&
                atoms[i].getAttribute ('hidden') != 'true')
                elements.push (atoms[i]);
        }
    }
    else if (kind == 'molecules') {
        var elements = document.getElementsByAttribute ('brailchem-mol-name', 'true');
        if (current_is_atom && ! first_move)
            current = document.getElementById (current.getAttribute ('brailchem-mol-id'));
    }
    else {
        alert ("Invalid move kind: " + kind);
        return;
    }
    var index = 0;    
    for (var i = 0; i < elements.length; i++)
        if (elements[i] == current) {
            index = i + (forward == null ? 0 : forward ? 1 : -1);
            break;
        }
    if (index < 0) {
        message_id = (kind == 'molecules' ? 'brailchemMoleculeNoPreviousMolecule' : 'brailchemMoleculeNoPreviousAtom');
        brailchem_message (message_id, 'brailchem-molecule-strings');
        return;
    }
    if (index >= elements.length) {
        message_id = (kind == 'molecules' ? 'brailchemMoleculeNoNextMolecule' : 'brailchemMoleculeNoNextAtom');
        brailchem_message (message_id, 'brailchem-molecule-strings');
        return;
    }
    brailchem_mol_focus (elements[index], true);
    if (kind == 'atoms')
        brailchem_focus(elements[index], true);
    else
        brailchem_mol_atom_focus(elements[index]);
}

function brailchem_mol_move_atom (forward)
{
    brailchem_mol_move_object (forward, 'atoms');
}

function brailchem_mol_next_atom ()
{
    brailchem_mol_move_atom (true);
}

function brailchem_mol_previous_atom ()
{
    brailchem_mol_move_atom (false);
}

function brailchem_mol_move_molecule (forward)
{
    brailchem_mol_move_object (forward, 'molecules');
}

function brailchem_mol_next_molecule ()
{
    brailchem_mol_move_molecule (true);
}

function brailchem_mol_previous_molecule ()
{
    brailchem_mol_move_molecule (false)
}

function brailchem_mol_go_reaction ()
{
    if (brailchem_mol_last_reaction_element) {
        brailchem_mol_focus (brailchem_mol_last_reaction_element);
        brailchem_focus (brailchem_mol_last_reaction_element, true);
    }
}

function brailchem_follow_reference (element)
{
    var id = element.getAttribute ('brailchem-target');
    var target = document.getElementById (id);
    brailchem_mol_focus (target);
    brailchem_mol_atom_focus (target);
}
