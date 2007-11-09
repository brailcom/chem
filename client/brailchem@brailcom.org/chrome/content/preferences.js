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
    brailchem_switch_page ('chrome://brailchem/content/preferences.xul', 'brailchem-preferences-window', brailchem_update_preferences,
                           'brailchem-preferences');
}

function brailchem_update_preferences ()
{
    // Server
    var host = brailchem_preferences.char ('server.host');
    var port = brailchem_preferences.int ('server.port');
    this.find_element ('pref-brailchem-host').setAttribute ('value', host);;
    this.find_element ('pref-brailchem-port').setAttribute ('value', port);    
    // General
    // It is quite tricky to select XUL menu item during frame initialization.
    // Any better method known?
    var language = brailchem_preferences.char ('language');
    var replaceable_node = this.document.getElementById ('pref-language-first');
    var menu_node = this.document.getElementById ('pref-language-menu');
    replaceable_node.setAttribute ('value', '*');
    replaceable_node.setAttribute ('label', menu_node.getElementsByAttribute ('value', language)[0].getAttribute ('label'));
    replaceable_node.setAttribute ('value', language);
    menu_node.getElementsByAttribute ('value', language)[0].setAttribute ('selected', 'true');
    // Periodic table
    var periodic_walk_over_empty = (brailchem_preferences.int ('periodic.walk_over_empty') ? 'true' : 'false');
    this.find_element ('pref-brailchem-periodic-emptycell').setAttribute ('checked', periodic_walk_over_empty);
    brailchem_periodic_update_tooltip_settings_node (this.find_element ('pref-brailchem-periodic-tooltips'));
}

function brailchem_set_preferences (close_window)
{
    // General
    var language = document.getElementById ('pref-language').value;
    if (language && language != '*')
        brailchem_preferences.set_char ('language', language);
    // Server
    brailchem_preferences.set_char ('server.host', document.getElementById ('pref-brailchem-host').value);
    brailchem_preferences.set_int ('server.port', document.getElementById ('pref-brailchem-port').value);
    // Periodic
    var periodic_walk_over_empty = (document.getElementById ('pref-brailchem-periodic-emptycell').getAttribute ('checked') == 'true' ? 1 : 0);
    brailchem_preferences.set_int ('periodic.walk_over_empty', periodic_walk_over_empty);
    var periodic_tooltip_box = document.getElementById ('pref-brailchem-periodic-tooltips');
    var tooltip_node_list = periodic_tooltip_box.getElementsByTagName ('checkbox');
    if (tooltip_node_list.length > 0) {
        var periodic_tooltips = [];
        for (var i = 0; i < tooltip_node_list.length; i++)
            if (tooltip_node_list[i].getAttribute ('checked') == 'true')
                periodic_tooltips.push (tooltip_node_list[i].getAttribute ('brailchem_property_name'));
        brailchem_preferences.set_char ('periodic.tooltips', periodic_tooltips.join (':'));
    }
    // all done
    if (close_window)
        window.close ();
}
