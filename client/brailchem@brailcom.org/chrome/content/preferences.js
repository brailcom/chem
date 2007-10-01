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
