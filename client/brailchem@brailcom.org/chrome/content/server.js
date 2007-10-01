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
