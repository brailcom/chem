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

var VERSION = '0.1';

function brailchem_help (section)
{
    var url = 'chrome://brailchem/locale/help.html';
    if (section)
        url = url + '#' + section;
    window.open (url, 'brailchem-help');
}

function brailchem_help_homepage ()
{
    window.open ('http://ict.brailcom.org/brailchem', 'brailchem-help');
}

function brailchem_help_about ()
{
    var text = brailchem_string ('brailchemSoftwareVersion', 'brailchem-strings') + ' ' + VERSION + '\n\n';        
    text += brailchem_read_url ('chrome://brailchem/locale/about.text');
    var stamp = brailchem_read_url ('chrome://brailchem/content/VERSION');
    if (stamp)
        text += brailchem_string ('brailchemBuildVersion', 'brailchem-strings') + ' ' + stamp + '\n\n';
    brailchem_report (brailchem_string ('brailchemAboutTitle', 'brailchem-strings'), text);
}
