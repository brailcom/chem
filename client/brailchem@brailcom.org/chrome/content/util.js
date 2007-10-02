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

// DOM handling

function brailchem_map_element (func, element)
{
    var children = element.childNodes;
    for (i = 0; i < children.length; i++)
        if (func (children[i]))
            return true;
    return false;
}

function brailchem_filter_element (func, element)
{
    children = [];
    function filter (element)
    {
        if (func (element))
            children.push (element);
    }
    brailchem_map_element (filter, element);
    return children;
}

function brailchem_add_element (parent, tag, attributes, text)
{
    var child = parent.ownerDocument.createElement (tag);
    if (attributes) {
        for (name in attributes)
            child.setAttribute (name, attributes[name]);
    }
    if (text != undefined) {
        child.appendChild (document.createCDATASection (text))
    }
    parent.appendChild (child);
    return child;
}

function brailchem_remove_children (node)
{
    while (node.hasChildNodes ())
        node.removeChild (node.childNodes[0]);
}

// Page switching

var BrailchemPage = {
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
        this.frame = document.getElementById ("brailchem-frame");
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
        if (page._after_display_function)
            page._after_display_function ();
        if (primary_element)
            brailchem_focus (primary_element);
        return true;
    },
};
    
function brailchem_page (uri, primary_element_id)
{
    this._uri = uri;
    this._primary_element_id = (primary_element_id == undefined ? 'brailchem-primary' : primary_element_id);
}
brailchem_page.prototype = BrailchemPage;

function brailchem_switch_page (uri, primary_element_id, after_function)
{
    var page = new brailchem_page (uri, primary_element_id);
    page.display (after_function);
    return page;
}

// Miscellaneous

function brailchem_focus (element)
{
    // The following seems to move both focus and the caret position in an
    // acceptable way
    var dispatcher = document.commandDispatcher;
    element.focus ();
    dispatcher.advanceFocusIntoSubtree (element);
}

// Preference handling

var brailchem_preferences = {
    
    _preferences: false,

    _default_values: {
        'server.host': 'www.brailcom.org', 'server.port': 8000,
        'display.preferred_views': 'ATOM_SYMBOL;NAME',
    },
    
    initialize_preferences: function () 
    {
        var prefs = Components.classes["@mozilla.org/preferences-service;1"].getService(Components.interfaces.nsIPrefService);
        this._preferences = prefs.getBranch ('brailchem.');
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