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
    brailchem_switch_page ("chrome://brailchem/content/periodic.xul", 'brailchem-periodic-window',
                           function () { brailchem_periodic_display (this); });
}
var g_element_data = null;
var g_language = null;
var g_tooltips = null;
var g_last_element = {main: null, extra: null};
var g_empty_walk = false;
var g_element_groups = null;
var g_oxidation_numbers = null;
var g_filter_conditions = {};

var brailchem_periodic_filter_keymap = {'e': brailchem_periodic_go_electronegativity_filter,
                                        'g': brailchem_periodic_go_group_filter,
                                        'o': brailchem_periodic_go_oxidation_filter,
                                       };

function brailchem_periodic_display (page)
{
    var strings = document.getElementById ('brailchem-periodic-strings');
    brailchem_message (strings.getString ('brailchemPeriodicPleaseWait'));
    g_tooltips = null;
    brailchem_periodic_update_data ();
    var element_data = g_element_data;
    // Any problem?
    if (element_data == null)
        return;
    // Prepare data
    var row_max = 0, col_max = 0;
    var extra_row_min = 1000, extra_row_max = 0, extra_col_min = 1000, extra_col_max = 0;
    var table = [];
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
    }
    // Render the table
    var empty_cell_string = strings.getString ('brailchemPeriodicEmptyCell');
    var row_string = strings.getString ('brailchemPeriodicRow');
    var column_string = strings.getString ('brailchemPeriodicColumn');
    var empty_walk = brailchem_preferences.int ('periodic.walk_over_empty');
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
                                                               disabled: (element || empty_walk ? 'false' : 'true'),
                                                               onfocus: focus_variable + '=this; brailchem_periodic_show_tooltip(this);',
                                                               brailchem_row: row, brailchem_column: col});
                if (element) {
                    var symbol = element['ATOM_SYMBOL'].value;
                    dom_element_node.setAttribute ('label', symbol);
                    dom_element_node.setAttribute ('brailchem-element-symbol', symbol);
                    dom_element_node.setAttribute ('style', '-moz-appearance: none; background-color: ' + element['_color'].value);
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
    // Update filter selectors
    var group_menu_node = page.find_element ('brailchem-setting-filter-group-menu');
    function removal_condition (element)
    {
        return element.tagName != 'menuitem' || element.getAttribute ('brailchem-noremove') != 'true';
    }
    brailchem_remove_children (group_menu_node, removal_condition);
    for (var group in g_element_groups)
        brailchem_add_element (group_menu_node, 'menuitem', {label: group, oncommand: "brailchem_periodic_group_filter('"+group+"')"});
    var oxidation_menu_node = page.find_element ('brailchem-setting-filter-oxidation-menu');
    brailchem_remove_children (oxidation_menu_node, removal_condition);
    var oxidation_list = [];
    for (var number in g_oxidation_numbers)
        oxidation_list.push (number);
    oxidation_list.sort (function (x0, y0) { var x = parseInt(x0), y = parseInt(y0); return (x==y ? 0 : (x<y ? -1 : 1)); });
    for (var i in oxidation_list) {
        var number = oxidation_list[i];
        brailchem_add_element (oxidation_menu_node, 'menuitem', {label: number, oncommand: "brailchem_periodic_oxidation_filter('"+number+"')"});
    }
    brailchem_message (strings.getString ('brailchemPeriodicDone'));
}

function brailchem_periodic_update_data ()
{
    if (g_language != brailchem_preferences.char ('language'))
        g_element_data = null;
    if (g_tooltips == null)
        brailchem_periodic_init_tooltips ();
    if (g_element_data == null)
        brailchem_periodic_update_element_data ();
}

function brailchem_periodic_init_tooltips ()
{
    var periodic_enabled_tooltips = brailchem_preferences.char ('periodic.tooltips').split (':');
    tooltips = {};
    for (var i in periodic_enabled_tooltips)
        tooltips[periodic_enabled_tooltips[i]] = true;
    g_tooltips = tooltips;
}

function brailchem_periodic_update_tooltip_settings_node (tooltips_node)
{
    brailchem_periodic_update_data ();
    brailchem_remove_children (tooltips_node);
    var property_names = {};
    for (var symbol in g_element_data) {
        var properties = g_element_data[symbol];
        for (var p in properties)
            property_names[properties[p].name] = true;
    }
    var properties_as_list = [];
    for (var p in property_names)
        if (properties[p])
            properties_as_list.push (properties[p]);    
    properties_as_list.sort (function (x0, y0) { var x = x0.name, y = y0.name; return (x==y ? 0 : (x<y ? -1 : 1)); });
    var tooltips = brailchem_preferences.char ('periodic.tooltips').split (':');
    for (var i = 0; i < properties_as_list.length; i++) {
        var item = properties_as_list[i];
        var name = item.name;
        if (name[0] != '_')
            brailchem_add_element (tooltips_node, 'checkbox',
                                   {label: item.label, checked: (tooltips.indexOf (name) != -1), brailchem_property_name: name});
    }
}

function brailchem_periodic_update_element_data ()
{
    var doc = brailchem_call_server ('periodic');
    if (doc == null)
        return;
    var data = {};
    var groups = {};
    var oxidation_numbers = {};
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
            if (p.hasAttribute ('value')) {
                var value = p.getAttribute ('value');
            }
            else {
                var value_items = p.getElementsByTagName ('listvalue')[0].getElementsByTagName ('value');
                var value = [];
                for (var k = 0; k < value_items.length; k++)
                    value.push (value_items[k].getAttribute ('value'));
            }
            properties[name] = {name: name, label: p.getAttribute ('label'), value: value};
        }
        var group = properties['ELEMENT_GROUP'];
        if (group)
            groups[group.value] = true;
        var oxidation_number_list = properties['OX_NUMBERS'].value;
        for (var j = 0; j < oxidation_number_list.length; j++)
            oxidation_numbers[oxidation_number_list[j]] = true;
        data[symbol] = properties;
    }
    g_element_data = data;
    g_element_groups = groups;
    g_oxidation_numbers = oxidation_numbers;
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
        var first_item = true;
        for (var j in tooltips)
            if (tooltips[j]) {
                tooltip = tooltip + (first_item ? '' : '\n') + element[j].label + ': ' + element[j].value;
                first_item = false;
            }
        element_node.setAttribute ('tooltiptext', tooltip);
    }
}

function brailchem_periodic_filter (conditions)
{
    var node_list = document.getElementsByTagName ('element');
    for (var i = 0; i < node_list.length; i++) {
        var element = node_list[i];
        var enabled = true;
        for (var j in conditions)
            if (! conditions[j] (element)) {
                enabled = false;
                break;
            }
        if (enabled) {
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

function brailchem_periodic_show_tooltip (element) 
{
    var tooltip_text = element.getAttribute ('tooltiptext');
    if (tooltip_text)
        brailchem_message (tooltip_text.replace ('\n', '; ', 'g'));
}

function brailchem_periodic_set_filter (enable)
{
    brailchem_periodic_update_data ();
    if (enable) {
        var conditions = [];
        for (var i in g_filter_conditions) {
            var c = g_filter_conditions[i];
            if (c != null)
                conditions.push (c);
        }
        brailchem_periodic_filter (conditions);
    }
    else
        brailchem_periodic_unfilter ();
}

function brailchem_periodic_group_filter (group)
{
    if (group) {
        function filter (element)
        {
            var symbol = element.getAttribute('brailchem-element-symbol');
            return g_element_data[symbol]['ELEMENT_GROUP'].value == group;
        }
        g_filter_conditions['group'] = filter;
        document.getElementById ('brailchem-setting-filter').setAttribute ('checked', 'true');
    }
    else
        g_filter_conditions['group'] = null;
    brailchem_periodic_set_filter (true);
}

function brailchem_periodic_oxidation_filter (oxidation_number)
{
    if (oxidation_number != null) {
        function filter (element)
        {
            var symbol = element.getAttribute('brailchem-element-symbol');
            var numbers = g_element_data[symbol]['OX_NUMBERS'].value;
            for (var i in numbers)
                if (numbers[i] == oxidation_number)
                    return true;
            return false;
        }
        g_filter_conditions['oxidation'] = filter;
        document.getElementById ('brailchem-setting-filter').setAttribute ('checked', 'true');
    }
    else
        g_filter_conditions['oxidation'] = null;
    brailchem_periodic_set_filter (true);
}

function brailchem_periodic_electronegativity_filter ()
{
    var from_value = parseFloat (document.getElementById ('electronegativity-from').value);
    var to_value = parseFloat (document.getElementById ('electronegativity-to').value);
    var empty = (! from_value && from_value != 0 && ! to_value && to_value != 0);
    if (empty)
        g_filter_conditions['electronegativity'] = null;
    else {
        if (! from_value && from_value != 0)
            from_value = -1000;
        if (! to_value && to_value != 0)
            to_value = 1000;
        function filter (element) 
        {
            var symbol = element.getAttribute('brailchem-element-symbol');
            var electronegativity = g_element_data[symbol]['EN'].value;
            return (from_value <= electronegativity && electronegativity <= to_value);
        }
        g_filter_conditions['electronegativity'] = filter;
        document.getElementById ('brailchem-setting-filter').setAttribute ('checked', 'true');
    }
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
    for (var name in properties)
        if (name[0] != '_') {
            var row = brailchem_add_element (top_node, 'row');
            var info = properties[name];
            brailchem_add_element (row, 'description', {value: info.label});
            brailchem_add_element (row, 'description', {}, info.value);
        }
    document.getElementById ('brailchem-element-details-box').setAttribute ('hidden', 'false');
    brailchem_focus (document.getElementById ('brailchem-element-details-box'));
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
    else
        brailchem_message (brailchem_string ('brailchemPeriodicNoNextElement', 'brailchem-periodic-strings'));
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
            brailchem_alert (strings.getString ('brailchemPeriodicNoActiveElement'));
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

function brailchem_periodic_go_electronegativity_filter ()
{
    brailchem_focus (document.getElementById ('brailchem-setting-filter-electronegativity-row'));
}

function brailchem_periodic_go_group_filter ()
{
    brailchem_focus (document.getElementById ('brailchem-setting-filter-group-row'));
}

function brailchem_periodic_go_oxidation_filter ()
{
    brailchem_focus (document.getElementById ('brailchem-setting-filter-oxidation-row'));
}

function brailchem_periodic_show_filtered_elements ()
{
    if (document.getElementById ('brailchem-setting-filter').getAttribute ('checked') != 'true') {
        var message = brailchem_string ('brailchemPeriodicNoFilter', 'brailchem-periodic-strings');
    }
    else {
        var message = '';
        var elements = document.getElementsByTagName ('element');
        for (var i = 0; i < elements.length; i++) {
            var node = elements[i];
            if (node.getAttribute ('disabled') != 'true')
                message = message + ' ' + node.getAttribute ('brailchem-element-symbol');
        }
    }
    brailchem_message (message);
}

function brailchem_periodic_jump_to_element ()
{
    var strings = document.getElementById ('brailchem-periodic-strings');
    var title = strings.getString ('brailchemPeriodicElementPromptTitle');
    var label = strings.getString ('brailchemPeriodicElementPromptLabel');
    // We have to perform some manual focus/defocus here to ensure proper refresh of defocused elements
    var focused_element = brailchem_defocus ();
    var symbol = brailchem_prompt (title, label);
    if (! symbol) {
        if (focused_element)
            focused_element.focus ();
        return;
    }
    symbol = symbol.toLowerCase ();
    var element_nodes = document.getElementsByTagName ('element');
    var target_node = null;
    for (var i = 0; i < element_nodes.length; i++) {
        var node = element_nodes[i];
        if (node.getAttribute ('brailchem-element-symbol').toLowerCase () == symbol) {
            target_node = node;
            break;
        }
    }
    if (target_node && target_node.getAttribute ('disabled') != 'true')
        brailchem_focus (target_node);
    else if (target_node) {
        brailchem_alert (brailchem_string ('brailchemPeriodicElementFiltered', 'brailchem-periodic-strings'));
        focused_element.focus ();
    }
    else {
        brailchem_alert (brailchem_string ('brailchemPeriodicInvalidSymbol', 'brailchem-periodic-strings'));
        focused_element.focus ();
    }
}
