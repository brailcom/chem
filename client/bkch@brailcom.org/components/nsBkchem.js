function BkchemComponent () {}

BkchemComponent.prototype = {

    error_string: null,
    get error_message () { return this.error_string; },
    
    fetch_xml: function (host, port, smiles) {
        this.error_string = null;
        var uri = 'http://' + host + ':' + port + '/smiles/' + encodeURIComponent(smiles);
        var req  = Components.classes["@mozilla.org/xmlextras/xmlhttprequest;1"].createInstance (Components.interfaces.nsIXMLHttpRequest);
        try {
            req.open ('GET', uri, false);
            req.send (null);
        }
        catch (e) {
            this.error_string = 'Connection to the bkchem HTTP server failed'
            return null;
        }
        if (req.status != 200)
            {
                this.error_string = 'Bkchem HTTP server returned error status ' + req.status;
                return null;
            }
        return req.responseXML;
    },
    
    QueryInterface: function (iid) {
        if (! iid.equals (Components.interfaces.nsIBkchem) &&
            ! iid.equals (Components.interfaces.nsISupports))
            {
                throw Components.results.NS_ERROR_NO_INTERFACE;
            }
        return this;
    }
};


var Module = {

    myCID: Components.ID ("{e9660d59-d076-40e9-bea6-3c8dc02c0ba1}"),
    myProgID: "@brailcom.org/bkch/bkchem;1",

    registerSelf: function (compMgr, fileSpec, location, type) {
        compMgr = compMgr.QueryInterface (Components.interfaces.nsIComponentRegistrar);
        compMgr.registerFactoryLocation (this.myCID, "Bkchem JS Component", this.myProgID, fileSpec, location, type);
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
            return (new BkchemComponent ()).QueryInterface (iid);
        }
    },

    canUnload: function (compMgr) {
        return true;
    }
}; // END Module

function NSGetModule (compMgr, fileSpec) { return Module; }
