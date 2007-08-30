function bkch_edit_preferences ()
{
    bkch_switch_page ("chrome://bkch/content/preferences.xul");
    var frame = document.getElementById ("bkch-frame");
    // The preferences.xul elements don't get accessible immediately, so we
    // have to use a timer to wait until they appear
    bkch_run_timer (function () { return bkch_update_preferences (frame); });
}

function bkch_update_preferences (frame)
{
    var document = frame.contentDocument;
    var host_field = document.getElementById ('pref-bkchem-host');
    if (! host_field)
        return false;
    var host = bkch_preferences.char ('server.host');
    var port = bkch_preferences.int ('server.port');
    host_field.setAttribute ('value', host);
    document.getElementById ('pref-bkchem-port').setAttribute ('value', port);
    var focus_element = document.getElementsByTagName ('window')[0];
    focus_element.focus ();
    return true;
}

function bkch_set_preferences ()
{
    bkch_preferences.set_char ('server.host', document.getElementById ('pref-bkchem-host').value);
    bkch_preferences.set_int ('server.port', document.getElementById ('pref-bkchem-port').value);
}
