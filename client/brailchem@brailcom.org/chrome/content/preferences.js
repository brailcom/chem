function brailchem_edit_preferences ()
{
    brailchem_switch_page ('chrome://brailchem/content/preferences.xul', 'brailchem-preferences-window', brailchem_update_preferences);
}

function brailchem_update_preferences ()
{
    var host = brailchem_preferences.char ('server.host');
    var port = brailchem_preferences.int ('server.port');
    this.find_element ('pref-brailchem-host').setAttribute ('value', host);;
    this.find_element ('pref-brailchem-port').setAttribute ('value', port);
}

function brailchem_set_preferences ()
{
    brailchem_preferences.set_char ('server.host', document.getElementById ('pref-brailchem-host').value);
    brailchem_preferences.set_int ('server.port', document.getElementById ('pref-brailchem-port').value);
}
