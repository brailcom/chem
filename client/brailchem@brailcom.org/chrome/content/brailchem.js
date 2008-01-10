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

function brailchem_start ()
{
    open ('chrome://brailchem/content/brailchem.xul', 'brailchem', 'chrome');
}

function brailchem_new_window ()
{
    // We must make the window name unique otherwise current window is simply
    // reused.  As I don't know how to share (in a reasonable way) global
    // variables of all application windows, we do this hack.  Of course it
    // doesn't make window name necessarily unique, but it works for intended
    // uses of the function.
    var window_name = 'brailchem' + (new Date().getTime()) + Math.random();
    open ('chrome://brailchem/content/brailchem.xul', window_name, 'chrome');
}

function brailchem_init ()
{
    addEventListener ('focus', brailchem_focus_callback, true);
    brailchem_message ('brailchemStarted', 'brailchem-strings');
    var argument = window.location.search;
    if (argument) {
        argument = argument.substring (1);
        var eq_pos = argument.indexOf ('=');
        if (eq_pos != -1) {
            var name = argument.substring (0, eq_pos);
            var value = argument.substring (eq_pos + 1);
            if (name == 'smiles')
                brailchem_molecule (value);
        }
    }
}

// Commands

function brailchem_quit ()
{
    window.close ();
}

function brailchem_upgrade ()
{
    var version = brailchem_read_url ('chrome://brailchem/content/VERSION');
    var remote_version = brailchem_read_url ('http://www.freebsoft.org/pub/projects/brailchem/VERSION');
    if (version == null || version < remote_version)
        open ('http://www.freebsoft.org/pub/projects/brailchem/brailchem.xpi');
    else
        brailchem_alert (brailchem_string ('brailchemNewestVersion', 'brailchem-strings'));
}
