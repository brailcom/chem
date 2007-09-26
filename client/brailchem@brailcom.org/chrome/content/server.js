function brailchem_call_server (func, argument)
{
    netscape.security.PrivilegeManager.enablePrivilege ("UniversalXPConnect");
    var brailchem = Components.classes["@brailcom.org/brailchem/brailchem;1"].createInstance (Components.interfaces.nsIBrailchem);
    if (! brailchem) {
        alert ("brailchem component not found!");
        return null;
    }
    var doc = brailchem.fetch_xml (brailchem_preferences.char ('server.host'), brailchem_preferences.int ('server.port'), func, argument);
    if (doc == null) {
        alert (brailchem.error_message);
    }
    return doc;
}
