var bkch_prefs;

function bkch_init_preferences ()
{
    if (! bkch_prefs) {
        var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
        bkch_prefs = prefs.getBranch ('bkchem.');
    }
}

function bkch_get_char_pref (pref, default_value)
{
    try {
        var result = bkch_prefs.getCharPref (pref);
    }
    catch (e) {
        bkch_prefs.setCharPref (pref, default_value);
        result = default_value;
    }
    return result;
}

function bkch_get_int_pref (pref, default_value)
{
    try {
        var result = bkch_prefs.getIntPref (pref);
    }
    catch (e) {
        bkch_prefs.setIntPref (pref, default_value);
        result = default_value;
    }
    return result;
}

function bkch_switch_page (uri)
{
    var frame = document.getElementById ("bkch-frame");
    frame.setAttribute ('src', uri);
}

function bkch_periodic_table ()
{
    bkch_switch_page ("chrome://bkch/content/periodic.xul");
}

function bkch_preferences ()
{
    bkch_switch_page ("chrome://bkch/content/preferences.xul");
    var frame = document.getElementById ("bkch-frame");
    // The preferences.xul elements don't get accessible immediately, so we
    // have to use a timer to wait until they appear
    var timer = Components.classes['@mozilla.org/timer;1'].createInstance (Components.interfaces.nsITimer);
    var callback =
    {
        notify: function (timer) {
            if (bkch_update_preferences (frame))
                timer.cancel ()
        }
    }
    timer.initWithCallback (callback, 100, timer.TYPE_REPEATING_SLACK);
}

function bkch_update_preferences (frame)
{
    bkch_init_preferences ();
    var host = bkch_get_char_pref ('server.host', 'localhost');
    var port = bkch_get_int_pref ('server.port', 8000);
    var document = frame.contentDocument;
    var host_field = document.getElementById ('pref-bkchem-host');
    if (! host_field)
        return false;
    host_field.setAttribute ('value', host);
    document.getElementById ('pref-bkchem-port').setAttribute ('value', port);
    return true;
}

function bkch_set_preferences ()
{
    bkch_init_preferences ();
    bkch_prefs.setCharPref ('server.host', document.getElementById ('pref-bkchem-host').value);
    bkch_prefs.setIntPref ('server.port', document.getElementById ('pref-bkchem-port').value);
}

function bkch_molecule ()
{
    bkch_switch_page ("chrome://bkch/content/molecule.xul");
    bkch_update_molecule ();
}

function bkch_update_molecule ()
{
    var smiles = document.getElementById ('molecule-textbox').value;
    var frame = document.getElementById ('bkch-frame');
    bkch_display_molecule (frame, smiles);
}

function bkch_remove_children (node)
{
    while (node.hasChildNodes ())
        node.removeChild (node.childNodes[0]);
}

function bkch_display_molecule (frame, smiles)
{
    // Fetch data
    bkch_init_preferences ();
    netscape.security.PrivilegeManager.enablePrivilege ("UniversalXPConnect");
    var bkchem = Components.classes["@brailcom.org/bkch/bkchem;1"].createInstance (Components.interfaces.nsIBkchem);
    if (! bkchem) {
        alert ("bkchem component not found!");
        return false;
    }
    var doc = bkchem.fetch_xml (bkch_get_char_pref ('server.host', 'localhost'), bkch_get_int_pref ('server.port', 8000), smiles);
    if (doc == null) {
        alert (bkchem.error_message);
        return false;
    }
    // Remove old contents
    var top_box = frame.contentDocument.getElementById ('molecule-display-box');
    bkch_remove_children (top_box);
    // Display data
    var element = doc.documentElement;
    bkch_display_element (element, top_box, 1);
}

function bkch_display_element (element, box, level)
{
    // Get node's contents
    var value, views, parts, neighbors;
    for (var index = 0; index < element.childNodes.length; index++) {
        var child = element.childNodes[index];
        if (child.nodeName == 'value')
            value = child.childNodes[0].nodeValue;
        else if (child.nodeName == 'views')
            views = child.childNodes;
        else if (child.nodeName == 'parts')
            parts = child.childNodes;
        else if (child.nodeName == 'neighbors')
            {
                neighbors = [];
                for (var i = 0; i < child.childNodes.length; i++)
                    if (child.childNodes[i] instanceof Element)
                        neighbors.push (child.childNodes[i]);
            }        
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
    // Utility functions for displaying
    var document = box.ownerDocument;
    function make_description (text, style)
    {
        var description = document.createElement ('description');
        description.appendChild (document.createCDATASection (text));
        if (style)
            description.setAttribute ('class', style);
        return description;
    }
    function make_section (caption)
    {
        var box = document.createElement ('vbox');
        var header = make_description (caption, 'header');
        box.appendChild (header);
        return box;
    }
    function add_element (element, box)
    {
        box.appendChild (element);
        return element;
    }
    // Show label or a property pair
    if (level > 6)
        level = 6;
    if (has_no_subparts) {
        if (value != undefined)
            add_element (make_description (label+': '+value, null), box);
        return;
    }
    if (value != undefined)
        label = value;
    add_element (make_description (label, 'header'), box);
    // Views
    if (views && views.length > 0) {
        var view_box = add_element (make_section ('Views', 'header'), box);
        for (var i = 0; i < views.length; i++)
            bkch_display_element (views[i], view_box, level+1);
    }
    // Neighbors
    if (neighbors && neighbors.length > 0) {
        var neighbor_box = add_element (make_section ('Neighbors', 'header'), box);
        for (var i = 0; i < neighbors.length; i++)
            add_element (make_description (neighbors[i].getAttribute ('id')), neighbor_box);
    }
    // Parts
    if (parts && parts.length > 0) {
        var part_box = add_element (make_section ('Parts', 'header'), box);
        for (var i = 0; i < parts.length; i++)
            bkch_display_element (parts[i], part_box, level+1);
    }
}
