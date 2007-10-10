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
import grp
import pwd
import xml.dom.minidom

import twisted.application.internet
import twisted.application.service
import twisted.internet
import twisted.web.resource
import twisted.web.server

from brailchem.session import Session
from brailchem.object_types import *
import brailchem.chem_reader
import brailchem.data_types
import brailchem.detail_periodic_table

### Chemical server communication

class ChemInterface(object):
    """Brailchem server interface."""

    def __init__(self, *args, **kwargs):
        super(ChemInterface, self).__init__(self, *args, **kwargs)
        self._session = Session(1)
        self._periodic_table_xml = None

    # DOM utilities

    def _create_dom(self):
        return xml.dom.minidom.Document()
    
    def _add_dom_element(self, dom, node, tag, attributes={}, text=None):
        element = dom.createElement(tag)
        for name, value in attributes.items():
            attribute = dom.createAttribute(name)
            element.setAttributeNode(attribute)
            element.setAttribute(name, unicode(value))
        if text is not None:
            element.appendChild(dom.createTextNode(unicode(text)))
        node.appendChild(element)
        return element
        
    # Chemical data processing
        
    def _retrieve_molecule_data(self, smiles):
        session = self._session
        data = session.process_string(smiles, format="SMILES")
        return data

    def _chem_to_dom(self, data):
        dom = self._create_dom()
        def add_element(*args, **kwargs):
            return self._add_dom_element(dom, *args, **kwargs)
        def transform(data, node):
            data_type = data.data_type()
            id = data.id()
            data_type_id = data_type.id()
            description = data_type.description()
            long_description = data_type.long_description()
            attributes = dict(id=id, type=data_type_id, description=description, long=long_description)
            data_node = add_element(node, 'data', attributes=attributes)
            if isinstance(data, Value):
                value = data.value()
                if isinstance(value, dict):
                    translated_value = value['en'] or value['cs'] or ''
                else:
                    translated_value = value
                add_element(data_node, 'value', text=translated_value)
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

    def _make_periodic_table_dom(self):
        periodic_table = brailchem.detail_periodic_table.symbol2properties
        info_provider = brailchem.data_types.DataTypeFactory()
        dom = self._create_dom()
        def add_element(*args, **kwargs):
            return self._add_dom_element(dom, *args, **kwargs)
        root = add_element(dom, 'periodic')
        for symbol, properties in periodic_table.items():
            element = add_element(root, 'element', attributes={'symbol': symbol})
            property_ids = [brailchem.chem_reader.ChemReader.table_key_to_data_type.get(name, name) for name in properties.keys()]
            property_labels = [(id, (info_provider.data_type_from_id(name) or brailchem.data_types.DataType(name, name)),)
                               for id, name in zip (properties.keys(), property_ids)]
            def keyfunction(x):
                return brailchem.data_types.DataType.default_priority(x[1])
            property_labels.sort(key=keyfunction, reverse=True)
            for property_key, info in property_labels:
                name = info.id()
                value = properties[property_key]
                if isinstance(value, dict):
                    translated_value = value['en'] or value['cs'] or ''
                else:
                    translated_value = value
                attributes = {'name': name,
                              'value': translated_value,
                              'label': info and info.description() or name,
                              }
                add_element(element, 'property', attributes=attributes)
        return dom
        
    # Public methods

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

    def periodic_table_xml(self):
        """Return periodic table data as an XML unicode.
        """
        if self._periodic_table_xml is None:
            dom = self._make_periodic_table_dom()
            xml = dom.toprettyxml(' ')
            self._periodic_table_xml = xml
        return self._periodic_table_xml

### HTTP output interface

class WebTree(twisted.web.resource.Resource):
    """Top-level web resource."""

    def __init__(self, service):
        twisted.web.resource.Resource.__init__(self)
        self._service = service
        self.putChild('smiles', SmilesWebResource(service))
        self.putChild('periodic', PeriodicWebResource(service))

class XMLWebResource(twisted.web.resource.Resource):

    def __init__(self, service):
        twisted.web.resource.Resource.__init__(self)
        self._service = service

    def _cb_render_GET(self, xml_string, request):
        data = codecs.getencoder('utf-8')(xml_string)[0]
        request.setHeader("content-type", 'application/xml')
        request.setHeader("content-length", str(len(data)))
        request.write(data)
        request.finish()    

class SmilesWebResource(XMLWebResource):
    """SMILES request web handler."""

    isLeaf = True

    _default_smiles = 'Oc1ccccc1C'

    def render_GET(self, request):
        if request.postpath:
            smiles = request.postpath[0]
        else:
            smiles = self._default_smiles
        defer = twisted.internet.defer.succeed(self._service.molecule_details_xml(smiles))
        defer.addCallback(self._cb_render_GET, request)
        return twisted.web.server.NOT_DONE_YET

class PeriodicWebResource(XMLWebResource):
    """Periodic table data."""
    
    isLeaf = True
        
    def render_GET(self, request):
        defer = twisted.internet.defer.succeed(self._service.periodic_table_xml())
        defer.addCallback(self._cb_render_GET, request)
        return twisted.web.server.NOT_DONE_YET

### Application setup

def make_service(config):
    uid = pwd.getpwnam(config['user']).pw_uid
    gid = grp.getgrnam(config['group']).gr_gid
    application = twisted.application.service.Application('brailchem', uid=uid, gid=gid)
    service_collection = twisted.application.service.IServiceCollection(application)
    tcp_server = twisted.application.internet.TCPServer(int(config['port']), twisted.web.server.Site(WebTree(ChemInterface())))
    tcp_server.setServiceParent(service_collection)
    return service_collection
