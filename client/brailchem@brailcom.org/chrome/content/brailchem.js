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

function brailchem_jump_to_subframe ()
{    
    var frame = document.getElementById ('brailchem-frame');
    var node_to_focus = brailchem_current_page.document.getElementById (brailchem_current_page.primary_element_id);
    brailchem_focus (node_to_focus);
}
