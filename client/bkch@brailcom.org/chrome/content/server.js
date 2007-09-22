function bkch_call_server (func, argument)
{
    netscape.security.PrivilegeManager.enablePrivilege ("UniversalXPConnect");
    var bkchem = Components.classes["@brailcom.org/bkch/bkchem;1"].createInstance (Components.interfaces.nsIBkchem);
    if (! bkchem) {
        alert ("bkchem component not found!");
        return null;
    }
    var doc = bkchem.fetch_xml (bkch_preferences.char ('server.host'), bkch_preferences.int ('server.port'), func, argument);
    if (doc == null) {
        alert (bkchem.error_message);
    }
    return doc;
}
