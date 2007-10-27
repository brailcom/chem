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
    brailchem_switch_page ('chrome://brailchem/content/molecule.xul', 'molecule-display-box');
}

function brailchem_browse_molecule ()
{
    var smiles = document.getElementById ('molecule-textbox').value;
    brailchem_update_molecule (smiles);
}

function brailchem_update_molecule (smiles)
{    
    brailchem_display_molecule (smiles);
    document.getElementsByTagName ('description')[0].focus ();
}

function brailchem_display_molecule (smiles)
{
    brailchem_wait_start ();
    // Fetch data
    var doc = brailchem_call_server ('smiles', smiles);
    if (doc == null)
        return;
    // Remove old contents
    var top_box = document.getElementById ('molecule-display-box');
    brailchem_remove_children (top_box);
    // Display data
    var element = doc.documentElement;
    if (element.nodeName == 'inputerror')
        brailchem_display_error (element.childNodes[0].nodeValue);
    else {
        var references = [], labels = {};
        brailchem_display_element (element, top_box, 1, references, labels);
        brailchem_backpatch_references (references, labels);
    }
    brailchem_wait_end ();
}

function brailchem_display_element (element, box, header_level, references, labels)
{
    // Utility functions for displaying
    var document = box.ownerDocument;
    function make_description (text, style, use_value)
    {
        var description = document.createElement ('description');
        if (! text)
            null;
        else if (use_value)
            description.setAttribute ('value', text);
        else
            description.appendChild (document.createCDATASection (text));
        if (style)
            description.setAttribute ('class', style);
        return description;
    }
    function make_section (caption, level, header_id)
    {
        var box = document.createElement ('vbox');
        var header = make_description (caption, 'header');
        header.setAttribute ('style', '-moz-user-focus: normal;');
        if (level)
            header.setAttribute ('level', level);
        if (header_id)
            header.setAttribute ('id', header_id);
        box.appendChild (header);
        return box;
    }
    function make_group (caption)
    {
        var box = document.createElement ('groupbox');
        var header = document.createElement ('caption');
        header.setAttribute ('label', caption);
        box.appendChild (header);
        return box;
    }
    function add_element (element, box)
    {
        box.appendChild (element);
        return element;
    }
    function element_text (element) {
        var text = element.childNodes[0].nodeValue;
        for (var i = 0; i < text.length; i++) {
            ch = text.charAt (i);
            if (ch != ' ' && ch != '\n')
                break;
        }
        if (i > 0)
            text = text.substring (i);
        return text;
        for (var i = text.length; i > 0; i--) {
            ch = text.charAt (i-1);
            if (ch != ' ' && ch != '\n')
                break;
        }
        if (i < text.length)
            text = text.substring (0, i);
        return text;
    }
    function element_value (element)
    {
        var children = element.childNodes;
        for (var i = 0; i < children.length; i++) {
            if (children[i].nodeName == 'value')
                return element_text (children[i]);
        }
        return null;
    }
    // Get node's contents
    var value, neighbors, parts;
    var views = [];
    var parts_as_views = [];
    for (var index = 0; index < element.childNodes.length; index++) {
        var child = element.childNodes[index];
        if (child.nodeName == 'value')
            value = element_text (child);
            //value = child.childNodes[0].nodeValue;
        else if (child.nodeName == 'views') {
            for (var i = 0; i < child.childNodes.length; i++) {
                var c = child.childNodes[i];
                // just a hack to handle complex views for now
                if (brailchem_map_element (function (element) { return element.nodeName == 'parts'; }, c))
                    parts_as_views.push (c);
                else
                    views.push (c);
            }
        }
        else if (child.nodeName == 'neighbors')
            neighbors = brailchem_filter_element (function (element) { return element instanceof Element; }, child);
        else if (child.nodeName == 'parts')
            parts = child.childNodes;
    }
    // How much is the node empty?
    var has_no_subparts = ((views == undefined || views.length == 0) &&
                           (parts == undefined || parts.length == 0) &&
                           (neighbors == undefined || neighbors.length == 0));
    if (! has_no_subparts) {
        function look_for_subparts (element) {
            if (! element)
                return false;
            if (! (element instanceof Element))
                return look_for_subparts (element.nextSibling);
            var tag = element.nodeName;
            if (tag == 'value' || tag == 'link')
                return true;
            if (look_for_subparts (element.firstChild))
                return true;
            return look_for_subparts (element.nextSibling);
        }
        has_no_subparts = ! look_for_subparts (element.firstChild);
    }
    if (value == undefined && has_no_subparts)
        return;
    var label = element.getAttribute ('description');
    // Show label or a property pair
    if (has_no_subparts) {
        if (value != undefined)
            add_element (make_description (label+': '+value, null), box);
        return;
    }
    if (value != undefined)
        label = value;
    else if (views) {
        var preferred_views = brailchem_preferences.char ('display.preferred_views').split (';');
        var chosen_label_index = 10000;
        for (var i = 0; i < views.length; i++) {
            var view = views[i];
            if (view.nodeName == 'data') {
                var value = element_value (view);
                if (value) {
                    var type = view.getAttribute ('type');
                    if (type) {
                        for (var j = 0; j < preferred_views.length && j < chosen_label_index; j++)
                            if (preferred_views[j] == type) {
                                label = value;
                                chosen_label_index = j;
                                break;
                            }
                    }
                }
            }
        }
    }
    var brailchem_id = element.getAttribute ('id');
    var displayed_element = add_element (make_section (label, header_level, brailchem_id), box);
    labels[brailchem_id] = label;
    // Views
    if (views && views.length > 0) {
        var view_box = add_element (make_group ("Properties"), box);
        for (var i = 0; i < views.length; i++)
            brailchem_display_element (views[i], view_box, header_level, references, labels);
    }
    // Neighbors
    if (neighbors && neighbors.length > 0) {
        var neighbor_box = add_element (make_group ("References"), box);
        for (var i = 0; i < neighbors.length; i++) {
            var id = neighbors[i].getAttribute ('id');
            var reference_element = add_element (document.createElement ('brailchemreference'), neighbor_box);
            reference_element.setAttribute ('brailchem-reference', id);
            references.push (reference_element);
        }
    }
    // Parts
    if (parts && parts.length > 0) {
        for (var i = 0; i < parts.length; i++)
            brailchem_display_element (parts[i], box, header_level+1, references, labels);
    }
    // Parts disguised as views
    if (parts_as_views) {
        for (var i = 0; i < parts_as_views.length; i++)
            brailchem_display_element (parts_as_views[i], box, header_level+1, references, labels);
    }
}

function brailchem_backpatch_references (references, labels)
{
    for (var i = 0; i < references.length; i++) {
        var reference_element = references[i];
        var brailchem_id = reference_element.getAttribute ('brailchem-reference');
        try {
            var label = labels[brailchem_id];
        }
        catch (e) {
            label = null;
        }
        if (label) {
            reference_element.setAttribute ('value', '*'+label);
            reference_element.setAttribute ('class', 'brailchem-reference');
        }
    }
}

function brailchem_follow_reference (element)
{
    var reference = element.getAttribute ('brailchem-reference');
    var document = element.ownerDocument;
    var target = document.getElementById (reference);
    brailchem_focus (target);
}
