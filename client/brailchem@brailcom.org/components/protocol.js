/* Copyright (C) 2008 Brailcom, o.p.s.

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

// Administrative stuff

const kSCHEME = "brailchem";
const kPROTOCOL_NAME = "Brailchem Protocol";
const kPROTOCOL_CONTRACTID = "@mozilla.org/network/protocol;1?name=" + kSCHEME;
const kPROTOCOL_CID = Components.ID("3432f556-8a16-11dd-807a-2f7c8c12adf2");

const kSIMPLEURI_CONTRACTID = "@mozilla.org/network/simple-uri;1";
const kIOSERVICE_CONTRACTID = "@mozilla.org/network/io-service;1";
const nsISupports = Components.interfaces.nsISupports;
const nsIIOService = Components.interfaces.nsIIOService;
const nsIProtocolHandler = Components.interfaces.nsIProtocolHandler;
const nsIURI = Components.interfaces.nsIURI;

var ProtocolFactory = new Object();

ProtocolFactory.createInstance = function (outer, iid)
{
    if (outer != null)
        throw Components.results.NS_ERROR_NO_AGGREGATION;
    if (! iid.equals (nsIProtocolHandler) &&
        ! iid.equals (nsISupports))
        throw Components.results.NS_ERROR_NO_INTERFACE;
    return new Protocol();
}

var BrailchemModule = new Object();

BrailchemModule.registerSelf = function (compMgr, fileSpec, location, type)
{
    compMgr = compMgr.QueryInterface (Components.interfaces.nsIComponentRegistrar);
    compMgr.registerFactoryLocation (kPROTOCOL_CID,
                                     kPROTOCOL_NAME,
                                     kPROTOCOL_CONTRACTID,
                                     fileSpec, 
                                     location, 
                                     type);
}
    
BrailchemModule.getClassObject = function (compMgr, cid, iid)
{
    if (! cid.equals (kPROTOCOL_CID))
        throw Components.results.NS_ERROR_NO_INTERFACE;
    if (! iid.equals (Components.interfaces.nsIFactory))
        throw Components.results.NS_ERROR_NOT_IMPLEMENTED;
    return ProtocolFactory;
}

BrailchemModule.canUnload = function (compMgr)
{
    return true;
}

function NSGetModule (compMgr, fileSpec)
{
    return BrailchemModule;
}

function Protocol () {}

Protocol.prototype =
{
    QueryInterface: function(iid)
    {
        if (! iid.equals (nsIProtocolHandler) &&
            ! iid.equals (nsISupports))
            throw Components.results.NS_ERROR_NO_INTERFACE;
        return this;
    },

    scheme: kSCHEME,
    defaultPort: -1,
    protocolFlags: nsIProtocolHandler.URI_NORELATIVE | nsIProtocolHandler.URI_NOAUTH,
  
    allowPort: function (port, scheme)
    {
        return false;
    },

    newURI: function (spec, charset, baseURI)
    {
        var uri = Components.classes[kSIMPLEURI_CONTRACTID].createInstance (nsIURI);
        uri.spec = spec;
        return uri;
    },

    // Here is the actual protocol implementation:
    newChannel: function (aURI)
    {
        // Examples of the URIs:
        // brailchem:SMILES=CC(=O)
        // brailchem:SMILES=http://www.example.com/something.smiles

        var uri = aURI.spec;
        var argument = uri.substring (uri.indexOf (':') + 1);        
        var ios = Components.classes[kIOSERVICE_CONTRACTID].getService (nsIIOService);
        var channel = ios.newChannel('chrome://brailchem/content/brailchem.xul?'+argument, null, null);
        return channel;
    },
}
