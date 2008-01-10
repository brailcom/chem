/* Copyright (C) 2007, 2008 Brailcom, o.p.s.

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
        child.appendChild (child.ownerDocument.createCDATASection (text))
    }
    parent.appendChild (child);
    return child;
}

function brailchem_set_element_text (node, text)
{
    brailchem_remove_children (node);
    node.appendChild (node.ownerDocument.createCDATASection (text));
}

function brailchem_remove_children (node, condition)
{
    var child_nodes = node.childNodes;
    for (var i = child_nodes.length - 1; i >= 0; i--) {
        var child = child_nodes[i];
        if (! condition || condition (child))
            node.removeChild (child);
    }
}

// Page switching

var brailchem_current_page = null;

var BrailchemPage = {
    _frame: null,
    _window: null,
    display_timer_interval: 100,
    get document() { return (this._frame ? this._frame.contentDocument : this._window.document); },
    get primary_element_id() { return this._primary_element_id },
    data: {},
    // Public methods
    find_element: function (element_id)
    {
        return this.document.getElementById (element_id);
    },
    display: function (after_function, window_name)
    {
        if (window_name) {
            this._window = open (this._uri, window_name, 'chrome');
        }
        else {
            brailchem_wait_start ();
            this._frame = document.getElementById ("brailchem-frame");
            // Clear the frame; it is necessary to clear global data otherwise
            // weird things may happen in case this is actually a restart of an
            // already running application.
            this._frame.setAttribute ('src', '');
            this._frame.setAttribute ('src', this._uri);
        }
        this._after_display_function = after_function;
        if (this._primary_element_id || after_function)
            // The frame elements often don't appear immediately, so we have to use
            // a timer to wait until they get available
            this.run_timer (this._display_callback, this._frame != null);
        else if (this._frame != null)
            brailchem_wait_end ();
    },
    run_timer: function (callback, report_finish)
    {
        var timer = Components.classes['@mozilla.org/timer;1'].createInstance (Components.interfaces.nsITimer);
        var page = this;
        var callback_object =
        {
            notify: function (timer) {
                if (callback (page)) {
                    timer.cancel ();
                    if (report_finish)
                        brailchem_wait_end ();
                }
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

function brailchem_switch_page (uri, primary_element_id, after_function, window_name)
{
    brailchem_current_page = new brailchem_page (uri, primary_element_id);
    brailchem_current_page.display (after_function, window_name);
    return brailchem_current_page;
}

// Focus

var brailchem_scroller = null;
var brailchem_scrollbox = null;

function brailchem_scrollto (element)
{    
    if (brailchem_scrollbox == null) {
        brailchem_scrollbox = document.getElementById ('brailchem-scrollbox');
        if (! brailchem_scrollbox)
            return;
    }
    if (brailchem_scroller == null)
        brailchem_scroller = brailchem_scrollbox.boxObject.QueryInterface (Components.interfaces.nsIScrollBoxObject);
    // Scrolling is somewhat overcomplicated because:
    // - brailchem_scroller.ensureElementIsVisible doesn't work at all
    // - brailchem_scroller.scrollToElement scrolls only in the vertical direction
    // - it's not obvious how to determine exact size of the available area
    var scroll_x = {}, scroll_y = {};
    brailchem_scroller.getPosition (scroll_x, scroll_y);
    var x1 = element.boxObject.x - scroll_x.value - brailchem_scrollbox.boxObject.x;
    var x2 = x1 + element.boxObject.width;
    var y1 = element.boxObject.y - scroll_y.value - brailchem_scrollbox.boxObject.y;
    var y2 = y1 + element.boxObject.height;
    var dx = 0, dy = 0;
    var scrollbar_width = 20; // approximately
    var available_width = brailchem_scrollbox.boxObject.width - scrollbar_width;
    var available_height = brailchem_scrollbox.boxObject.height - scrollbar_width;
    if (y1 < 0)
        dy = y1;
    else if (y2 > available_height)
        dy = y2 - available_height;
    if (x1 < 0)
        dx = x1;
    else if (x2 > available_width)
        dx = x2 - available_width;
    if (dy || dx)
        brailchem_scroller.scrollBy (dx, dy);
}

function brailchem_focus_callback ()
{
    brailchem_scrollto (document.commandDispatcher.focusedElement);
    document.getElementById ('brailchem-heading').setAttribute ('brailchem-active', 'true');
    var iframe = document.getElementById ('brailchem-frame');
    var other_document = (iframe ? iframe.contentDocument : parent.document);
    other_document.getElementById ('brailchem-heading').setAttribute ('brailchem-active', 'false');
}

function brailchem_focus (element, subtree)
{
    element.focus ();
    if (subtree) {
        // The following seems to move both focus and the caret position in an
        // acceptable way.  Additionally it serves for special cases like
        // focusing elements inside XBL widgets etc.
        var dispatcher = document.commandDispatcher;
        dispatcher.advanceFocusIntoSubtree (element);
    }
}

function brailchem_defocus ()
{
    var focused = document.commandDispatcher.focusedElement;
    if (focused)
	focused.blur();
    return focused;
}

// Preference handling

var brailchem_preferences = {
    
    _preferences: false,

    _default_values: {
        'server.host': 'www.brailcom.org', 'server.port': 8000,
        'language': 'en',
        'display.preferred_views': 'ATOM_SYMBOL;NAME',
        'periodic.walk_over_empty': 0,
        'periodic.tooltips': 'ELEMENT_NAME',
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
};

// Command key sequence handling

var g_current_keymap = null;

function brailchem_set_keymap (keymap)
{
    g_current_keymap = keymap;
    brailchem_defocus ();
}

function brailchem_process_key (event)
{
    if (g_current_keymap == null)
        return;    
    var key = String.fromCharCode (event.charCode).toLowerCase ();
    var command = g_current_keymap[key];
    g_current_keymap = null;
    if (command) {
        event.preventDefault ();
        event.preventBubble ();
        command ();
    }
}

// Echo area

function brailchem_echo_area ()
{
    return document.getElementById ('brailchem-echo-area') || parent.document.getElementById ('brailchem-echo-area');
}

function brailchem_message (message, string_element)
{
    if (string_element)
        message = brailchem_string (message, string_element);
    brailchem_echo_area ().label = message || '';
}

function brailchem_clear_message ()
{
    brailchem_echo_area ().label = '';
}

// Dialogs

function brailchem_alert (message)
{
    brailchem_report (brailchem_string ('brailchemErrorWindow', 'brailchem-strings'), message);
}

function brailchem_report (title, message)
{
    var prompt_service = Components.classes["@mozilla.org/embedcomp/prompt-service;1"].getService (Components.interfaces.nsIPromptService);
    prompt_service.alert (window, title, message);
}

function brailchem_prompt (title, label)
{
    var prompt_service = Components.classes["@mozilla.org/embedcomp/prompt-service;1"].getService (Components.interfaces.nsIPromptService);
    var input = {value: ''};
    var result = prompt_service.prompt (window, title, label, input, null, {value: false});
    return (result ? input.value : null);
}

// IO

function brailchem_read_url (url)
{
    try {
        // Taken from http://forums.mozillazine.org/viewtopic.php?p=921150#921150
        var io_service = Components.classes["@mozilla.org/network/io-service;1"].getService (Components.interfaces.nsIIOService);
        var scriptable_stream = Components.classes["@mozilla.org/scriptableinputstream;1"]
                                .getService (Components.interfaces.nsIScriptableInputStream);
        var channel = io_service.newChannel (url, null, null);
        var input = channel.open ();
        scriptable_stream.init (input);
        var text = scriptable_stream.read (input.available ());
        scriptable_stream.close ();
        input.close ();
    }
    catch (e) {
        return null;
    }
    return text;
}

// Miscelaneous

function brailchem_string (string, string_element)
{
    var strings = document.getElementById (string_element);
    return strings.getString (string);
}

function brailchem_check_float_input (element)
{
    var value = element.value;
    if (value == '' || value == '-' || value == '+')
        return;
    var float_value = parseFloat (value);
    var new_value = (float_value || float_value == '0' ? float_value.toString () : '');
    if ((value[0] == '+' || value[0] == '-') &&
        (new_value.length == 0 || (new_value[0] != '+' && new_value[0] != '-')))
        new_value = value[0] + new_value;
    if (value[value.length-1] == '.')
            new_value = new_value + '.';
    if (new_value != value)
        element.value = new_value;
}

function brailchem_wait_start ()
{
    brailchem_message ('brailchemGlobalPleaseWait', 'brailchem-strings');
}

function brailchem_wait_end ()
{
    brailchem_message ('brailchemGlobalDone', 'brailchem-strings');
}
