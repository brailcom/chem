function bkch_edit_preferences ()
{
    bkch_switch_page ('chrome://bkch/content/preferences.xul', 'bkch-preferences-window', bkch_update_preferences);
}

function bkch_update_preferences ()
{
    var host = bkch_preferences.char ('server.host');
    var port = bkch_preferences.int ('server.port');
    this.find_element ('pref-bkchem-host').setAttribute ('value', host);;
    this.find_element ('pref-bkchem-port').setAttribute ('value', port);
}

function bkch_set_preferences ()
{
    bkch_preferences.set_char ('server.host', document.getElementById ('pref-bkchem-host').value);
    bkch_preferences.set_int ('server.port', document.getElementById ('pref-bkchem-port').value);
}
