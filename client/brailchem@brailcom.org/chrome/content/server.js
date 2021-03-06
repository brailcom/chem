/* Copyright (C) 2007, 2008, 2014 Brailcom, o.p.s.

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

function BrailchemComponent () {}

BrailchemComponent.prototype = {

    error_string: null,
    get error_message () { return this.error_string; },
    
    fetch_xml: function (host, port, function_name, arguments) {
        this.error_string = null;
        var uri = 'http://' + host + ':' + port + '/' + function_name;
        var boundary = '--------XX' + Math.random();
        var full_boundary = '--' + boundary + '\r\n';
        var data = '';
        for (var i = 0; i < arguments.length; i++) {
            var argument = arguments[i];
            data = data + full_boundary;
            data = data + 'Content-Disposition: form-data; name="' + argument.name + '"\r\n\r\n';
            data = data + argument.value + '\r\n';            
        }
        data = data + '--' + boundary + '--\r\n';
        var req  = Components.classes["@mozilla.org/xmlextras/xmlhttprequest;1"].createInstance (Components.interfaces.nsIXMLHttpRequest);
        try {
            req.open ('POST', uri, false);
            req.setRequestHeader ("Content-type", "multipart/form-data; boundary=" + boundary);
            req.setRequestHeader ("Content-length", data.length);
            req.sendAsBinary (data);
        }
        catch (e) {
            this.error_string = 'Connection to the Brailchem HTTP server failed'
            return null;
        }
        if (req.status != 200)
            {
                this.error_string = 'Brailchem HTTP server returned error status ' + req.status;
                return null;
            }
        return req.responseXML;
    }
};

function brailchem_call_server (func, arguments)
{
    var brailchem = new BrailchemComponent ();
    if (! arguments)
        arguments = [];
    arguments.push ({name: 'language', value: brailchem_preferences.char ('language')});
    var doc = brailchem.fetch_xml (brailchem_preferences.char ('server.host'), brailchem_preferences.int ('server.port'), func, arguments);
    if (doc == null) {
        alert (brailchem.error_message);
    }
    return doc;
}
