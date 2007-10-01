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

function BrailchemComponent () {}

BrailchemComponent.prototype = {

    error_string: null,
    get error_message () { return this.error_string; },
    
    fetch_xml: function (host, port, function_name, argument) {
        this.error_string = null;
        var uri = 'http://' + host + ':' + port + '/' + function_name;
        if (argument)
            uri = uri + '/' + encodeURIComponent(argument);
        var req  = Components.classes["@mozilla.org/xmlextras/xmlhttprequest;1"].createInstance (Components.interfaces.nsIXMLHttpRequest);
        try {
            req.open ('GET', uri, false);
            req.send (null);
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
    },
    
    QueryInterface: function (iid) {
        if (! iid.equals (Components.interfaces.nsIBrailchem) &&
            ! iid.equals (Components.interfaces.nsISupports))
            {
                throw Components.results.NS_ERROR_NO_INTERFACE;
            }
        return this;
    }
};


var Module = {

    myCID: Components.ID ("{e9660d59-d076-40e9-bea6-3c8dc02c0ba1}"),
    myProgID: "@brailcom.org/brailchem/brailchem;1",

    registerSelf: function (compMgr, fileSpec, location, type) {
        compMgr = compMgr.QueryInterface (Components.interfaces.nsIComponentRegistrar);
        compMgr.registerFactoryLocation (this.myCID, "Brailchem JS Component", this.myProgID, fileSpec, location, type);
    },

    getClassObject : function (compMgr, cid, iid) {
        if (! cid.equals (this.myCID))
            throw Components.results.NS_ERROR_NO_INTERFACE;
        if (! iid.equals (Components.interfaces.nsIFactory))
            throw Components.results.NS_ERROR_NOT_IMPLEMENTED;
        return this.myFactory;
    },

    myFactory: {
        createInstance: function (outer, iid) {
            if (outer != null)
                throw Components.results.NS_ERROR_NO_AGGREGATION;
            return (new BrailchemComponent ()).QueryInterface (iid);
        }
    },

    canUnload: function (compMgr) {
        return true;
    }
}; // END Module

function NSGetModule (compMgr, fileSpec) { return Module; }
