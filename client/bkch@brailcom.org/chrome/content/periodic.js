function bkch_periodic_table ()
{
    bkch_switch_page ("chrome://bkch/content/periodic.xul", 'bkch-periodic-window', bkch_periodic_display);
}

function bkch_periodic_display ()
{
    doc = bkch_call_server ('periodic');
    if (doc == null)
        return;
    if (! this.data.element_data) {
        this.data.tooltips = {'NAME_EN': true};    
        bkch_update_periodic_data (this, doc);
    }
    bkch_periodic_render (this);
}

function bkch_update_periodic_data (page, doc)
{
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
    page.data.element_data = data;
}

function bkch_periodic_render (page)
{
    var element_data = page.data.element_data;
    // Any problem?
    if (element_data == null)
        return;
    bkch_periodic_page = page;
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
    function render_table (top_node_id, row_min, row_max, col_min, col_max) {
        var top_node = page.find_element (top_node_id);
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
                var dom_element_node = bkch_add_element (dom_row_node, (element ? 'element' : 'xelement'), {class: 'bkch-element-button'});
                if (element) {
                    var symbol = element['ATOM_SYMBOL'];
                    dom_element_node.setAttribute ('label', symbol);
                    dom_element_node.setAttribute ('bkch-element-symbol', symbol);
                }
                else {
                    dom_element_node.setAttribute ('tooltiptext', "empty cell");
                }
            }
        }
    }
    render_table ('bkch-periodic-table-node', 1, row_max, 1, col_max);
    render_table ('bkch-periodic-extra-table-node', extra_row_min, extra_row_max, extra_col_min, extra_col_max);
    bkch_periodic_update_tooltips (page);
    // Update settings
    var tooltips_node = page.find_element ('bkch-tooltip-settings');
    var tooltips = page.data.tooltips;
    for (var i = 0; i < property_names_list.length; i++) {
        var name = property_names_list[i];
        var checkbox_node = bkch_add_element (tooltips_node, 'checkbox',
                                              {label: name, checked: tooltips[name], bkch_property_name: name,
                                               oncommand: 'bkch_periodic_set_tooltip(this)'});
        checkbox_node.addEventListener ('command', function (event) { bkch_periodic_set_tooltip (page, event.target); }, false);
    }
}

function bkch_periodic_update_tooltips (page)
{
    var tooltips = page.data.tooltips;
    var element_data = page.data.element_data;
    var element_nodes = page.document.getElementsByTagName ('element');
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

function bkch_periodic_set_tooltip (page, element)
{
    var property_name = element.getAttribute ('bkch_property_name');
    var value = element.checked;
    page.data.tooltips[property_name] = element.getAttribute('checked');
    bkch_periodic_update_tooltips (page);
}

// Commands

function bkch_element_command (event, command)
{
    command (event.currentTarget);
    event.stopPropagation ();
}

function bkch_element_info (element)
{
    alert ('info called!');
}

function bkch_element_left (element)
{
    alert ('left called!');
}

function bkch_element_right (element)
{
    alert ('right called!');
}

function bkch_element_down (element)
{
    alert ('down called!');
}

function bkch_element_up (element)
{
    alert ('up called!');
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
