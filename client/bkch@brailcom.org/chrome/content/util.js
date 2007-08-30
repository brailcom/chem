// DOM handling

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

function bkch_remove_children (node)
{
    while (node.hasChildNodes ())
        node.removeChild (node.childNodes[0]);
}

// Page switching

function bkch_switch_page (uri)
{
    var frame = document.getElementById ("bkch-frame");
    frame.setAttribute ('src', uri);
    return frame;
}

function bkch_run_timer (callback)
{
    var timer = Components.classes['@mozilla.org/timer;1'].createInstance (Components.interfaces.nsITimer);
    var callback_object =
    {
        notify: function (timer) {
            if (callback ())
                timer.cancel ()
        }
    }
    timer.initWithCallback (callback_object, 100, timer.TYPE_REPEATING_SLACK);
}

// Preference handling

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
