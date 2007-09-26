function bkch_periodic_table ()
{
    bkch_switch_page ("chrome://bkch/content/periodic.xul", 'bkch-periodic-window', function () { bkch_periodic_display (this); });
}

var bkch_periodic_element_data = null;
var bkch_periodic_tooltips = null;
var bkch_periodic_last_element = null;
var bkch_periodic_last_extra_element = null;

function bkch_periodic_display (page)
{
    bkch_periodic_update_data ();
    var element_data = bkch_periodic_element_data;
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
        var row = parseInt (properties['ROW']);
        var col = parseInt (properties['COLUMN']);
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
            property_names[p] = true;
    }
    var property_names_list = [];
    for (var p in property_names)
        property_names_list.push (p);
    property_names_list.sort ();
    // Render the table
    var strings = document.getElementById ('bkch-periodic-strings');
    var empty_cell_string = strings.getString ('bkchPeriodicEmptyCell');
    var row_string = strings.getString ('bkchPeriodicRow');
    var column_string = strings.getString ('bkchPeriodicColumn');
    function render_table (top_node_id, row_min, row_max, col_min, col_max, focus_variable) {
        var top_node = page.find_element (top_node_id);
        bkch_remove_children (top_node);
        var header_row = bkch_add_element (top_node, 'row');
        bkch_add_element (header_row, 'description');
        for (var col = col_min; col <= col_max; col++)
            bkch_add_element (header_row, 'description', {class: 'bkch-periodic-header', value: col});
        for (var row = row_min; row <= row_max; row++) {
            var table_row = table[row];
            var dom_row_node = bkch_add_element (top_node, 'row', {bkch_row_number: row});
            bkch_add_element (dom_row_node, 'description', {class: 'bkch-periodic-header', value: row});
            for (var col = col_min; col <= col_max; col++) {
                var element = table_row[col];
                var dom_element_node = bkch_add_element (dom_row_node, (element ? 'element' : 'xelement'),
                                                         {class: 'bkch-element-button',
                                                          id: 'bkch-element-' + row + '-' + col,
                                                          onfocus: focus_variable + '=this;',
                                                          bkch_row: row, bkch_column: col});
                if (element) {
                    var symbol = element['ATOM_SYMBOL'];
                    dom_element_node.setAttribute ('label', symbol);
                    dom_element_node.setAttribute ('bkch-element-symbol', symbol);
                }
                else {
                    var tooltip_text = empty_cell_string + ' (' + row_string + ' ' + row + ', ' + column_string + ' ' + col + ')';
                    dom_element_node.setAttribute ('tooltiptext', tooltip_text);
                }
            }
        }
    }
    render_table ('bkch-periodic-table-node', 1, row_max, 1, col_max, 'bkch_periodic_last_element');
    render_table ('bkch-periodic-extra-table-node', extra_row_min, extra_row_max, extra_col_min, extra_col_max, 'bkch_periodic_last_extra_element');
    bkch_periodic_update_tooltips (page.document);
    // Update settings
    var tooltips_node = page.find_element ('bkch-tooltip-settings');
    bkch_remove_children (tooltips_node);
    var tooltips = bkch_periodic_tooltips;
    for (var i = 0; i < property_names_list.length; i++) {
        var name = property_names_list[i];
        var checkbox_node = bkch_add_element (tooltips_node, 'checkbox',
                                              {label: name, checked: tooltips[name], bkch_property_name: name,
                                               oncommand: 'bkch_periodic_set_tooltip(event.target)'});
    }
}

function bkch_periodic_update_data ()
{
    if (bkch_periodic_element_data == null)
        bkch_periodic_update_element_data ();
    if (bkch_periodic_tooltips == null)
        bkch_periodic_init_tooltips ();
}

function bkch_periodic_init_tooltips ()
{
    bkch_periodic_tooltips = {'NAME_EN': true};
}

function bkch_periodic_update_element_data ()
{
    var doc = bkch_call_server ('periodic');
    if (doc == null)
        return;
    var data = {};
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
            properties[p.getAttribute ('name')] = p.getAttribute ('value');
        }
        data[symbol] = properties;
    }
    bkch_periodic_element_data = data;
}

function bkch_periodic_update_tooltips (doc_node)
{
    if (! doc_node)
        doc_node = document;
    bkch_periodic_update_data ();
    var element_data = bkch_periodic_element_data;
    var tooltips = bkch_periodic_tooltips;
    var element_nodes = doc_node.getElementsByTagName ('element');
    for (var i = 0; i < element_nodes.length; i++) {
        var element_node = element_nodes[i];
        var element = element_data[element_node.getAttribute ('bkch-element-symbol')];
        var tooltip = '';
        for (var j in tooltips)
            if (tooltips[j])
                tooltip = tooltip + j + ': ' + element[j] + '\n';
        element_node.setAttribute ('tooltiptext', tooltip);
    }
}

function bkch_periodic_filter (condition)
{
    var node_list = document.getElementsByTagName ('element');
    for (var i = 0; i < node_list.length; i++) {
        var element = node_list[i];
        if (condition (element))
            element.setAttribute ('bkch-emphasized', 'true');
        else
            element.setAttribute ('disabled', 'true');
    }
}

function bkch_periodic_unfilter ()
{
    var node_list = document.getElementsByTagName ('element');
    for (var i = 0; i < node_list.length; i++) {
        var element = node_list[i]
        element.setAttribute ('disabled', 'false');
        element.setAttribute ('bkch-emphasized', 'false');
    }
}

// Callbacks

function bkch_periodic_set_tooltip (element)
{
    bkch_periodic_update_data ();
    var property_name = element.getAttribute ('bkch_property_name');
    var value = element.checked;
    bkch_periodic_tooltips[property_name] = element.getAttribute('checked');
    bkch_periodic_update_tooltips ();
}

// Commands

function bkch_element_command (event, command)
{
    command (event.currentTarget);
    event.stopPropagation ();
}

function bkch_element_info (element)
{
    bkch_periodic_update_data ();
    var symbol = element.getAttribute ('bkch-element-symbol');
    var top_node = document.getElementById ('bkch-element-details');
    bkch_remove_children (top_node);
    var properties = bkch_periodic_element_data[symbol];
    for (var name in properties) {
        var row = bkch_add_element (top_node, 'row');
        bkch_add_element (row, 'description', {value: name})
        bkch_add_element (row, 'description', {value: properties[name]})
    }
    bkch_focus (document.getElementById ('bkch-element-info'));
}

function bkch_element_move (element, row_increment, col_increment)
{
    var row = parseInt (element.getAttribute ('bkch_row')) + row_increment;
    var col = parseInt (element.getAttribute ('bkch_column')) + col_increment;
    var table = document.getElementById (col < 100 ? 'bkch-periodic-table-node' : 'bkch-periodic-extra-table-node');
    function find_child (tag)
    {
        var children = table.getElementsByTagName (tag);
        for (var i = 0; i < children.length; i++) {
            var candidate = children[i];
            if (candidate.getAttribute ('bkch_row') == row && candidate.getAttribute ('bkch_column') == col)
                return candidate;
        }
        return null;
    }
    var target = find_child ('element') || find_child ('xelement');
    if (target)
        bkch_focus (target);
}

function bkch_element_left (element)
{
    bkch_element_move (element, 0, -1);
}

function bkch_element_right (element)
{
    bkch_element_move (element, 0, 1);
}

function bkch_element_down (element)
{
    bkch_element_move (element, 1, 0);
}

function bkch_element_up (element)
{
    bkch_element_move (element, -1, 0);
}

function bkch_element_electrons (element)
{
}

function bkch_element_group (element)
{
}

function bkch_element_period (element)
{
}

function bkch_element_related (element)
{
}

function bkch_periodic_go_table ()
{
    if (! bkch_periodic_last_element)
        bkch_periodic_last_element = document.getElementById ('bkch-periodic-table-node').getElementsByTagName ('element')[0];
    bkch_focus (bkch_periodic_last_element);
}

function bkch_periodic_go_extra_table ()
{
    if (! bkch_periodic_last_extra_element)
        bkch_periodic_last_extra_element = document.getElementById ('bkch-periodic-extra-table-node').getElementsByTagName ('element')[0];
    bkch_focus (bkch_periodic_last_extra_element);
}

function bkch_periodic_go_settings ()
{
    bkch_focus (document.getElementById ('bkch-periodic-settings'));
}
