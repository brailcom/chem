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

function brailchem_periodic_table ()
{
    brailchem_switch_page ("chrome://brailchem/content/periodic.xul", 'brailchem-periodic-window', function () { brailchem_periodic_display (this); });
}

var g_element_data = null;
var g_tooltips = null;
var g_last_element = {main: null, extra: null};
var g_empty_walk = false;
var g_element_groups = null;
var g_filter_condition = function (element) { return true; }    

function brailchem_periodic_display (page)
{
    brailchem_periodic_update_data ();
    var element_data = g_element_data;
    // Any problem?
    if (element_data == null)
        return;
    // Prepare data
    var row_max = 0, col_max = 0;
    var extra_row_min = 1000, extra_row_max = 0, extra_col_min = 1000, extra_col_max = 0;
    var table = [];
    var property_names = {};
    for (var symbol in element_data) {
        var properties = element_data[symbol];
        var row = parseInt (properties['PERIODIC_TABLE_ROW'].value);
        var col = parseInt (properties['PERIODIC_TABLE_COLUMN'].value);
        if (col < 100) {
            if (row > row_max)
                row_max = row;
            if (col > col_max)
                col_max = col;
        }
        else {
            if (row < extra_row_min)
                extra_row_min = row;
            else if (row > extra_row_max)
                extra_row_max = row;            
            if (col < extra_col_min)
                extra_col_min = col;
            else if (col > extra_col_max)
                extra_col_max = col;
        }        
        table_row = table[row];
        if (! table_row)
            table_row = table[row] = [];
        table_row[col] = properties;
        for (var p in properties)
            property_names[properties[p].name] = true;
    }
    var properties_as_list = [];
    for (var p in property_names)
        if (properties[p])
            properties_as_list.push (properties[p]);    
    properties_as_list.sort (function (x0, y0) { var x = x0.name, y = y0.name; return (x==y ? 0 : (x<y ? -1 : 1)); });
    // Render the table
    var strings = document.getElementById ('brailchem-periodic-strings');
    var empty_cell_string = strings.getString ('brailchemPeriodicEmptyCell');
    var row_string = strings.getString ('brailchemPeriodicRow');
    var column_string = strings.getString ('brailchemPeriodicColumn');
    function render_table (top_node_id, row_min, row_max, col_min, col_max, focus_variable) {
        var top_node = page.find_element (top_node_id);
        brailchem_remove_children (top_node);
        var header_row = brailchem_add_element (top_node, 'row');
        brailchem_add_element (header_row, 'description');
        for (var col = col_min; col <= col_max; col++)
            brailchem_add_element (header_row, 'description', {class: 'brailchem-periodic-header', value: col});
        for (var row = row_min; row <= row_max; row++) {
            var table_row = table[row];
            var dom_row_node = brailchem_add_element (top_node, 'row', {brailchem_row_number: row});
            brailchem_add_element (dom_row_node, 'description', {class: 'brailchem-periodic-header', value: row});
            for (var col = col_min; col <= col_max; col++) {
                var element = table_row[col];
                var dom_element_node = brailchem_add_element (dom_row_node, (element ? 'element' : 'xelement'),
                                                              {class: 'brailchem-element-button',
                                                               id: 'brailchem-element-' + row + '-' + col,
                                                               disabled: (element || g_empty_walk ? 'false' : 'true'),
                                                               onfocus: focus_variable + '=this;',
                                                               brailchem_row: row, brailchem_column: col});
                if (element) {
                    var symbol = element['ATOM_SYMBOL'].value;
                    dom_element_node.setAttribute ('label', symbol);
                    dom_element_node.setAttribute ('brailchem-element-symbol', symbol);
                }
                else {
                    var tooltip_text = empty_cell_string + ' (' + row_string + ' ' + row + ', ' + column_string + ' ' + col + ')';
                    dom_element_node.setAttribute ('tooltiptext', tooltip_text);
                }
            }
        }
    }
    render_table ('brailchem-periodic-table-node', 1, row_max, 1, col_max, 'g_last_element.main');
    render_table ('brailchem-periodic-extra-table-node', extra_row_min, extra_row_max, extra_col_min, extra_col_max, 'g_last_element.extra');
    brailchem_periodic_update_tooltips (page.document);
    // Update settings
    var tooltips_node = page.find_element ('brailchem-tooltip-settings');
    brailchem_remove_children (tooltips_node);
    var tooltips = g_tooltips;
    properties_as_list.sort (function (x0, y0) { var x = x0.label, y = y0.label; return (x==y ? 0 : (x<y ? -1 : 1)); });
    for (var i = 0; i < properties_as_list.length; i++) {
        var item = properties_as_list[i];
        var name = item.name;
        var checkbox_node = brailchem_add_element (tooltips_node, 'checkbox',
                                                   {label: item.label, checked: tooltips[name], brailchem_property_name: name,
                                                    oncommand: 'brailchem_periodic_set_tooltip(event.target)'});
    }
    var group_menu_node = page.find_element ('brailchem-setting-filter-group-menu');
    brailchem_remove_children (group_menu_node);
    for (var group in g_element_groups)
        brailchem_add_element (group_menu_node, 'menuitem', {label: group, oncommand: "brailchem_periodic_group_filter('"+group+"')"});
}

function brailchem_periodic_update_data ()
{
    if (g_element_data == null)
        brailchem_periodic_update_element_data ();
    if (g_tooltips == null)
        brailchem_periodic_init_tooltips ();
}

function brailchem_periodic_init_tooltips ()
{
    g_tooltips = {'ELEMENT_NAME': true};
}

function brailchem_periodic_update_element_data ()
{
    var doc = brailchem_call_server ('periodic');
    if (doc == null)
        return;
    var data = {};
    var groups = {};
    var top_element = doc.documentElement;
    var elements = top_element.childNodes;
    for (var i = 0; i < elements.length; i++) {
        var elt = elements[i];
        if (elt.nodeName != 'element')
            // ignore text nodes
            continue;
        var symbol = elt.getAttribute ('symbol');
        var properties = {};
        var property_elements = elt.childNodes;
        for (var j = 0; j < property_elements.length; j++) {
            var p = property_elements[j];
            if (p.nodeName != 'property')
                // ignore text nodes
                continue;
            var name = p.getAttribute ('name');            
            properties[name] = {name: name, label: p.getAttribute ('label'), value: p.getAttribute ('value')};
        }
        var group = properties['ELEMENT_GROUP'];
        if (group)
            groups[group.value] = true;
        data[symbol] = properties;
    }
    g_element_data = data;
    g_element_groups = groups;
}

function brailchem_periodic_update_tooltips (doc_node)
{
    if (! doc_node)
        doc_node = document;
    brailchem_periodic_update_data ();
    var element_data = g_element_data;
    var tooltips = g_tooltips;
    var element_nodes = doc_node.getElementsByTagName ('element');
    for (var i = 0; i < element_nodes.length; i++) {
        var element_node = element_nodes[i];
        var element = element_data[element_node.getAttribute ('brailchem-element-symbol')];
        var tooltip = '';
        for (var j in tooltips)
            if (tooltips[j])
                tooltip = tooltip + element[j].label + ': ' + element[j].value + '\n';
        element_node.setAttribute ('tooltiptext', tooltip);
    }
}

function brailchem_periodic_filter (condition)
{
    var node_list = document.getElementsByTagName ('element');
    for (var i = 0; i < node_list.length; i++) {
        var element = node_list[i];
        if (condition (element)) {
            element.setAttribute ('disabled', 'false');
            element.setAttribute ('brailchem-emphasized', 'true');
        }
        else {
            element.setAttribute ('disabled', 'true');
            element.setAttribute ('brailchem-emphasized', 'true');
        }
    }
}

function brailchem_periodic_unfilter ()
{
    var node_list = document.getElementsByTagName ('element');
    for (var i = 0; i < node_list.length; i++) {
        var element = node_list[i]
        element.setAttribute ('disabled', 'false');
        element.setAttribute ('brailchem-emphasized', 'false');
    }
}

// Callbacks

function brailchem_periodic_set_tooltip (element)
{
    brailchem_periodic_update_data ();
    var property_name = element.getAttribute ('brailchem_property_name');
    var value = element.checked;
    g_tooltips[property_name] = element.getAttribute('checked');
    brailchem_periodic_update_tooltips ();
}

function brailchem_periodic_empty_cells (enabled)
{
    if ((g_empty_walk && ! enabled) || (! g_empty_walk && enabled)) {
        g_empty_walk = enabled;
        var value = (g_empty_walk ? 'false' : 'true');
        var xelements = document.getElementsByTagName ('xelement');
        for (var i = 0; i < xelements.length; i++)
            xelements[i].setAttribute ('disabled', value);
    }
}

function brailchem_periodic_set_filter (enable)
{
    brailchem_periodic_update_data ();
    if (enable)
        brailchem_periodic_filter (g_filter_condition);
    else
        brailchem_periodic_unfilter ();
}

function brailchem_periodic_group_filter (group)
{
    function filter (element)
    {
        var symbol = element.getAttribute('brailchem-element-symbol');
        return g_element_data[symbol]['ELEMENT_GROUP'].value == group;
    }    
    g_filter_condition = filter;
    document.getElementById ('brailchem-setting-filter').setAttribute ('checked', 'true');
    brailchem_periodic_set_filter (true);
}

// Commands

function brailchem_element_command (event, command)
{
    command (event.currentTarget);
    event.stopPropagation ();
}

function brailchem_element_info (element)
{
    brailchem_periodic_update_data ();
    var symbol = element.getAttribute ('brailchem-element-symbol');
    var top_node = document.getElementById ('brailchem-element-details');
    brailchem_remove_children (top_node);
    var properties = g_element_data[symbol];
    for (var name in properties) {
        var row = brailchem_add_element (top_node, 'row');
        var info = properties[name];
        brailchem_add_element (row, 'description', {value: info.label});
        brailchem_add_element (row, 'description', {}, info.value);
    }
    brailchem_focus (document.getElementById ('brailchem-element-info'));
}

function brailchem_element_move (element, row_increment, col_increment)
{
    var row = parseInt (element.getAttribute ('brailchem_row')) + row_increment;
    var col = parseInt (element.getAttribute ('brailchem_column')) + col_increment;
    var table = document.getElementById (col < 100 ? 'brailchem-periodic-table-node' : 'brailchem-periodic-extra-table-node');
    var elements = [];
    function add_nodelist (nodelist)
    {
        for (var i = 0; i < nodelist.length; i++) {
            var node = nodelist[i];
            if (node.getAttribute ('disabled') != 'true')
                elements.push (nodelist[i]);
        }
    }
    add_nodelist (table.getElementsByTagName ('element'));
    add_nodelist (table.getElementsByTagName ('xelement'));    
    var target = null;
    var target_row = (row_increment == 0 ? row : (row_increment < 0 ? -1000 : 1000));
    var target_col = (col_increment == 0 ? col : (col_increment < 0 ? -1000 : 1000));
    function update_target (node, row, col) 
    {
        target = node;
        target_row = row;
        target_col = col;
    }
    for (var i = 0; i < elements.length; i++) {
        var node = elements[i];
        var node_row = parseInt (node.getAttribute ('brailchem_row'));
        var node_col = parseInt (node.getAttribute ('brailchem_column'));
        if (row_increment == 0) {
            if (node_row != row)
                continue;
            if (col_increment < 0) {
                if (node_col <= col && node_col > target_col)
                    update_target (node, node_row, node_col);
            }
            else {              // col_increment > 0
                if (node_col >= col && node_col < target_col)
                    update_target (node, node_row, node_col);
            }
        }
        else {
            if (row_increment < 0 && (node_row > row || node_row < target_row))
                continue;
            if (row_increment > 0 && (node_row < row || node_row > target_row))
                continue;
            if (node_row != target_row ||
                (target_col > col && node_col < target_col) ||
                (target_col < col && node_col <= col && node_col > target_col))
                update_target (node, node_row, node_col);
        }
    }
    if (target)
        brailchem_focus (target);
}

function brailchem_element_left (element)
{
    brailchem_element_move (element, 0, -1);
}

function brailchem_element_right (element)
{
    brailchem_element_move (element, 0, 1);
}

function brailchem_element_down (element)
{
    brailchem_element_move (element, 1, 0);
}

function brailchem_element_up (element)
{
    brailchem_element_move (element, -1, 0);
}

function brailchem_element_electrons (element)
{
}

function brailchem_element_group (element)
{
}

function brailchem_element_period (element)
{
}

function brailchem_element_related (element)
{
}

function brailchem_periodic_go_table (table_node_id, last_element_field)
{
    var last_element = g_last_element[last_element_field];
    if (! last_element || last_element.getAttribute ('disabled') == 'true') {
        var table_node = document.getElementById (table_node_id);
        var element_nodes = table_node.getElementsByTagName ('element');
        var found = false;
        for (var i = 0; i < element_nodes.length; i++) {
            var node = element_nodes[i];
            if (node.getAttribute ('disabled') != 'true') {
                g_last_element[last_element_field] = node;
                found = true;
                break;
            }
        }
        if (! found) {
            var strings = document.getElementById ('brailchem-periodic-strings');
            alert (strings.getString ('brailchemPeriodicNoActiveElement'));
            return;
        }
    }
    brailchem_focus (g_last_element[last_element_field]);
}

function brailchem_periodic_go_main_table ()
{
    brailchem_periodic_go_table ('brailchem-periodic-table-node', 'main');
}

function brailchem_periodic_go_extra_table ()
{
    brailchem_periodic_go_table ('brailchem-periodic-extra-table-node', 'extra');
}

function brailchem_periodic_go_settings ()
{
    brailchem_focus (document.getElementById ('brailchem-periodic-settings'));
}
