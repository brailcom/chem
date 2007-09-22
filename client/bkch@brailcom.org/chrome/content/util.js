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

function bkch_add_element (parent, tag, attributes)
{
    var child = parent.ownerDocument.createElement (tag);
    if (attributes) {
        for (name in attributes)
            child.setAttribute (name, attributes[name]);
    }
    parent.appendChild (child);
    return child;
}

function bkch_remove_children (node)
{
    while (node.hasChildNodes ())
        node.removeChild (node.childNodes[0]);
}

// Page switching

var BkchPage = {
    frame: null,
    display_timer_interval: 100,
    get document() { return this.frame.contentDocument; },
    data: {},
    // Public methods
    find_element: function (element_id)
    {
        return this.frame.contentDocument.getElementById (element_id);
    },
    display: function (after_function)
    {
        this.frame = document.getElementById ("bkch-frame");
        this.frame.setAttribute ('src', this._uri);
        this._after_display_function = after_function;
        if (this._primary_element_id || after_function)
            // The frame elements often don't appear immediately, so we have to use
            // a timer to wait until they get available
            this.run_timer (this._display_callback);
    },
    run_timer: function (callback) 
    {
        var timer = Components.classes['@mozilla.org/timer;1'].createInstance (Components.interfaces.nsITimer);
        var page = this;
        var callback_object =
        {
            notify: function (timer) {
                if (callback (page))
                    timer.cancel ();
            }
        }
        timer.initWithCallback (callback_object, this.display_timer_interval, timer.TYPE_REPEATING_SLACK);    
    },
    // Private methods
    _display_callback: function (page)
    {
        // Strangely enough, `this' is not set correctly when called from a timer.
        // So we have to provide the `page' argument explicitly.
        var primary_id = page._primary_element_id;
        if (primary_id) {
            var primary_element = page.find_element (primary_id);
            if (! primary_element)
                return false;
        }
        if (primary_element)
            bkch_focus (primary_element);
        if (page._after_display_function)
            page._after_display_function ();
        return true;
    },
};
    
function bkch_page (uri, primary_element_id)
{
    this._uri = uri;
    this._primary_element_id = (primary_element_id == undefined ? 'bkch-primary' : primary_element_id);
}
bkch_page.prototype = BkchPage;

function bkch_switch_page (uri, primary_element_id, after_function)
{
    var page = new bkch_page (uri, primary_element_id);
    page.display (after_function);
    return page;
}

// Miscellaneous

function bkch_focus (element)
{
    // The following seems to move both focus and the caret position in an
    // acceptable way
    var dispatcher = document.commandDispatcher;
    element.focus ();
    dispatcher.advanceFocusIntoSubtree (element);
}

// Preference handling

var bkch_preferences = {
    
    _preferences: false,

    _default_values: {
        'server.host': 'www.brailcom.org', 'server.port': 8000,
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
