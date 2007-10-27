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
}

// Commands

function brailchem_quit ()
{
    window.close ();
}

function brailchem_upgrade ()
{
    window.open ('http://www.freebsoft.org/pub/projects/brailchem/brailchem.xpi');
}
