var bkch_preferences = {
    
    _preferences: false,

    _default_values: {
        'server.host': 'localhost', 'server.port': 8000,
        'display.preferred_views': 'ATOM_SYMBOL;NAME',
    },
    
    initialize_preferences: function () 
    {
        var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
        this._preferences = prefs.getBranch ('bkchem.');
    },

    _default_value: function (name)
    {
        if (! this._preferences)
            this.initialize_preferences ();
        return this._default_values[name];
    },

    _get_preference: function (name, reader, writer)
    {
        try {
            var result = reader (name);
        }
        catch (e) {
            result = this._default_value (name)
            writer (name, result);
        }
        return result;
    },

    char: function (name)
    {
        if (! this._preferences)
            this.initialize_preferences ();
        return this._get_preference (name, this._preferences.getCharPref, this._preferences.setCharPref);
    },
    
    int: function (name)
    {
        if (! this._preferences)
            this.initialize_preferences ();
        return this._get_preference (name, this._preferences.getIntPref, this._preferences.setIntPref);
    },

    set_char: function (name, value)
    {
        if (! this._preferences)
            this.initialize_preferences ();
        this._preferences.setCharPref (name, value);
    },
    
    set_int: function (name, value)
    {
        if (! this._preferences)
            this.initialize_preferences ();
        this._preferences.setIntPref (name, value);
    },
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

function bkch_edit_preferences ()
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
    var host = bkch_preferences.char ('server.host');
    var port = bkch_preferences.int ('server.port');
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
    bkch_preferences.set_char ('server.host', document.getElementById ('pref-bkchem-host').value);
    bkch_preferences.set_int ('server.port', document.getElementById ('pref-bkchem-port').value);
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

function bkch_element_value (element)
{
    var children = element.childNodes;
    for (var i = 0; i < children.length; i++) {
        if (children[i].nodeName == 'value')
            return children[i].childNodes[0].nodeValue;
    }
    return null;
}

function bkch_map_element (func, element)
{
    var children = element.childNodes;
    for (i = 0; i < children.length; i++)
        if (func (children[i]))
            return true;
    return false;
}

function bkch_filter_element (func, element)
{
    children = [];
    function filter (element)
    {
        if (func (element))
            children.push (element);
    }
    bkch_map_element (filter, element);
    return children;
}

function bkch_display_molecule (frame, smiles)
{
    // Fetch data
    netscape.security.PrivilegeManager.enablePrivilege ("UniversalXPConnect");
    var bkchem = Components.classes["@brailcom.org/bkch/bkchem;1"].createInstance (Components.interfaces.nsIBkchem);
    if (! bkchem) {
        alert ("bkchem component not found!");
        return false;
    }
    var doc = bkchem.fetch_xml (bkch_preferences.char ('server.host'), bkch_preferences.int ('server.port'), smiles);
    if (doc == null) {
        alert (bkchem.error_message);
        return false;
    }
    // Remove old contents
    var top_box = frame.contentDocument.getElementById ('molecule-display-box');
    bkch_remove_children (top_box);
    // Display data
    var element = doc.documentElement;
    bkch_display_element (element, top_box, 1, 1);
}

function bkch_display_element (element, box, header_level)
{
    // Get node's contents
    var value, neighbors, parts;
    var views = [];
    var parts_as_views = [];
    for (var index = 0; index < element.childNodes.length; index++) {
        var child = element.childNodes[index];
        if (child.nodeName == 'value')
            value = child.childNodes[0].nodeValue;
        else if (child.nodeName == 'views') {
            for (var i = 0; i < child.childNodes.length; i++) {
                var c = child.childNodes[i];
                // just a hack to handle complex views for now
                if (bkch_map_element (function (element) { return element.nodeName == 'parts'; }, c))
                    parts_as_views.push (c);
                else
                    views.push (c);
            }
        }
        else if (child.nodeName == 'neighbors')
            neighbors = bkch_filter_element (function (element) { return element instanceof Element; }, child);
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
    function make_section (caption, level)
    {
        var box = document.createElement ('vbox');
        var header = make_description (caption, 'header');
        if (level)
            header.setAttribute ('level', level);
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
    // Show label or a property pair
    if (has_no_subparts) {
        if (value != undefined)
            add_element (make_description (label+': '+value, null), box);
        return;
    }
    if (value != undefined)
        label = value;
    else if (views) {
        var preferred_views = bkch_preferences.char ('display.preferred_views').split (';');
        var chosen_label_index = 10000;
        for (var i = 0; i < views.length; i++) {
            var view = views[i];
            if (view.nodeName == 'data') {
                var value = bkch_element_value (view);
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
    add_element (make_section (label, header_level), box);
    // Views
    if (views && views.length > 0) {
        var view_box = add_element (make_group ("Properties"), box);
        for (var i = 0; i < views.length; i++)
            bkch_display_element (views[i], view_box, header_level);
    }
    // Neighbors
    if (neighbors && neighbors.length > 0) {
        var neighbor_box = add_element (make_group ("References"), box);
        for (var i = 0; i < neighbors.length; i++)
            add_element (make_description (neighbors[i].getAttribute ('id')), neighbor_box);
    }
    // Parts
    if (parts && parts.length > 0) {
        for (var i = 0; i < parts.length; i++)
            bkch_display_element (parts[i], box, header_level+1);
    }
    // Parts disguised as views
    if (parts_as_views) {
        for (var i = 0; i < parts_as_views.length; i++)
            bkch_display_element (parts_as_views[i], box, header_level+1);
    }
}
