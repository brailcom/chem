# Copyright (C) 2007 Brailcom, o.p.s.
#
# COPYRIGHT NOTICE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import codecs
import os
import urllib
import xml.dom.minidom

import twisted.application
import twisted.internet
import twisted.web.resource
import twisted.web.server
import zope.interface

import oasa

from chem_server import ChemServer
from object_types import *

### Chemical server communication

class ChemInterface(object):
    """Chem server interface."""

    def __init__(self, *args, **kwargs):
        super(ChemInterface, self).__init__(self, *args, **kwargs)
        self._server = ChemServer()

    def _retrieve_molecule_data(self, smiles):
        server = self._server
        session = server.connect()
        try:
            data = session.process_string(smiles, format="SMILES")
        finally:
            server.disconnect(session.number())
        return data

    def _chem_to_dom(self, data):
        dom = xml.dom.minidom.Document()
        def add_element(node, tag, attributes={}, text=None):
            element = dom.createElement(tag)
            for name, value in attributes.items():
                attribute = dom.createAttribute(name)
                element.setAttributeNode(attribute)
                element.setAttribute(name, unicode(value))
            if text is not None:
                element.appendChild(dom.createTextNode(unicode(text)))
            node.appendChild(element)
            return element
        def transform(data, node):
            data_type = data.data_type()
            id = data.id()
            data_type_id = data_type.id()
            description = data_type.description()
            long_description = data_type.long_description()
            attributes = dict(id=id, type=data_type_id, description=description, long=long_description)
            data_node = add_element(node, 'data', attributes=attributes)
            if isinstance(data, Value):
                add_element(data_node, 'value', text=data.value())
            if isinstance(data, Complex):
                parts_node = add_element(data_node, 'parts')
                for part in data.parts():
                    transform(part.target(), parts_node)
            if isinstance(data, Part):
                neighbors_node = add_element(data_node, 'neighbors')
                for neighbor in data.neighbors():
                    add_element(neighbors_node, 'link', attributes=dict(id=neighbor.target().id()))
            if isinstance(data, MultiView):
                views_node = add_element(data_node, 'views')
                for view in data.views():
                    transform(view, views_node)
        transform(data, dom)
        return dom

    def _molecule_dom(self, smiles):
        data = self._retrieve_molecule_data(smiles)
        dom = self._chem_to_dom(data)
        return dom
        
    def molecule_details(self, smiles):
        """Return information about the given molecule as a DOM object.

        Arguments:

          smiles -- molecule name as a string in the SMILES notation

        """
        dom = self._molecule_dom(smiles)
        return dom
    
    def molecule_details_xml(self, smiles):
        """Return information about the given molecule as an XML unicode.

        Arguments:

          smiles -- molecule name as a string in the SMILES notation

        """
        dom = self._molecule_dom(smiles)
        xml = dom.toprettyxml(' ')
        return xml

### HTTP output interface

class WebTree(twisted.web.resource.Resource):
    """Top-level web resource."""

    def __init__(self, service):
        twisted.web.resource.Resource.__init__(self)
        self._service = service
        self.putChild('smiles', SmilesWebResource(service))
    
class SmilesWebResource(twisted.web.resource.Resource):
    """SMILES request web handler."""

    isLeaf = True

    _default_smiles = 'Oc1ccccc1C'

    def __init__(self, service):
        twisted.web.resource.Resource.__init__(self)
        self._service = service

    def _cb_render_GET(self, xml_string, request):
        data = codecs.getencoder('utf-8')(xml_string)[0]
        request.setHeader("content-type", 'application/xml')
        request.setHeader("content-length", str(len(data)))
        request.write(data)
        request.finish()

    def render_GET(self, request):
        if request.postpath:
            smiles = request.postpath[0]
        else:
            smiles = self._default_smiles
        defer = twisted.internet.defer.succeed(self._service.molecule_details_xml(smiles))
        defer.addCallback(self._cb_render_GET, request)
        return twisted.web.server.NOT_DONE_YET

### Application setup

def make_service(config):
    application = twisted.application.service.Application('chem') #, uid=1, gid=1)
    service_collection = twisted.application.service.IServiceCollection(application)
    tcp_server = twisted.application.internet.TCPServer(config['port'], twisted.web.server.Site(WebTree(ChemInterface())))
    tcp_server.setServiceParent(service_collection)
    return service_collection
