# Copyright (C) 2007, 2008 Brailcom, o.p.s.
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
import copy
import grp
import pwd
import xml.dom.minidom
from sets import Set

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
import brailchem.i18n

### Chemical server communication

class ChemInterface(object):
    """Brailchem server interface."""

    def __init__(self, *args, **kwargs):
        super(ChemInterface, self).__init__(self, *args, **kwargs)
        self._session = Session(1)
        self._periodic_table_xml = {}
        self._language_list_xml = None

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

    def _make_translator(self, language):
        if language == '*':
            selected_language = 'en'
        else:
            selected_language = language
        return brailchem.i18n.GettextTranslator(selected_language, default_domain='brailchem', fallback=True)
        
    def _retrieve_molecule_data(self, chem_text, format="SMILES"):
        session = self._session
        data = session.process_string(chem_text, format=format)
        return data

    def _chem_to_dom(self, data, language):
        dom = self._create_dom()
        translator = self._make_translator(language)
        already_serialized = Set()
        def add_element(*args, **kwargs):
            return self._add_dom_element(dom, *args, **kwargs)
        def transform(data, node):
            data_type = data.data_type()
            id = data.id()
            # serialize only once, make references later
            if id in already_serialized:
                add_element(node,"ref", attributes=dict(id=id))
            else:
                already_serialized.add(id)
                data_type_id = data_type.id()
                description = data_type.description()
                if isinstance(description, brailchem.i18n.TranslatableText):
                    description = description.translate(translator)
                long_description = data_type.long_description()
                if isinstance(long_description, brailchem.i18n.TranslatableText):
                    long_description = long_description.translate(translator)
                attributes = dict(id=id, type=data_type_id, description=description, long=long_description, priority=data.priority())
                data_node = add_element(node, 'data', attributes=attributes)
                if isinstance(data, LanguageDependentValue):
                    value = data.value(language)[1]
                    add_element(data_node, 'value', text=value)
                elif isinstance(data, Value):
                    value = data.value()
                    if isinstance(value, list):
                        list_node = add_element(data_node, 'listvalue')
                        for list_item in value:
                            add_element(list_node, 'value', text=list_item)
                    else:
                        add_element(data_node, 'value', text=value)
                if isinstance(data, Complex):
                    parts_node = add_element(data_node, 'parts')
                    for part in data.parts():
                        transform(part.target(), parts_node)
                if isinstance(data, Part):
                    neighbors_node = add_element(data_node, 'neighbors')
                    for neighbor in data.neighbors():
                        neighbor_description = neighbor.data_type().description()
                        if isinstance(neighbor_description, brailchem.i18n.TranslatableText):
                            neighbor_description = neighbor_description.translate(translator)
                        attrs = neighbor.properties()
                        attrs.update(dict(id=neighbor.target().id(),
                                          description=neighbor_description,
                                          type=neighbor.data_type().id(),
                                          ))
                        add_element(neighbors_node, 'link', attributes=attrs)
                if isinstance(data, MultiView):
                    views_node = add_element(data_node, 'views')
                    for view in data.views():
                        transform(view, views_node)
        transform(data, dom)
        return dom

    def _molecule_dom(self, chem_text, format, language):
        data = self._retrieve_molecule_data(chem_text, format=format)
        dom = self._chem_to_dom(data, language)
        return dom

    def _make_periodic_table_dom(self, language):
        translator = self._make_translator(language)
        periodic_table = brailchem.detail_periodic_table.symbol2properties
        info_provider = brailchem.data_types.DataTypeFactory()
        dom = self._create_dom()
        def add_element(*args, **kwargs):
            return self._add_dom_element(dom, *args, **kwargs)
        root = add_element(dom, 'periodic')
        for symbol, properties in periodic_table.items():
            element = add_element(root, 'element', attributes={'symbol': symbol})
            properties = copy.copy(properties)
            properties['_color'] = brailchem.detail_periodic_table.group2color[properties['group']['en']]
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
                    translated_value = value.get(language, '') or value.get('en', '')
                else:
                    translated_value = value
                label = info and info.description() or name
                if isinstance(label, brailchem.i18n.TranslatableText):
                    label = label.translate(translator)
                attributes = {'name': name,
                              'label': label,
                              }
                if not isinstance(translated_value, list):
                    attributes['value'] = translated_value
                property_element = add_element(element, 'property', attributes=attributes)
                if isinstance(translated_value, list):
                    list_element = add_element(property_element, 'listvalue')
                    for item in translated_value:
                        add_element(list_element, 'value', attributes={'value': item})
        return dom

    # Public methods

    def molecule_details(self, chem_text, format, language):
        """Return information about the given molecule as a DOM object.

        Arguments:

          smiles -- molecule name as a string in the SMILES notation

        """
        dom = self._molecule_dom(chem_text, format, language)
        return dom
    
    def molecule_details_xml(self, chem_text, format, language):
        """Return information about the given molecule as an XML unicode.

        Arguments:

          smiles -- molecule name as a string in the SMILES notation

        """
        dom = self._molecule_dom(chem_text, format, language)
        xml = dom.toprettyxml(' ')
        return xml

    def periodic_table_xml(self, language):
        """Return periodic table data as an XML unicode.
        """
        if self._periodic_table_xml.get(language) is None:
            dom = self._make_periodic_table_dom(language)
            xml = dom.toprettyxml(' ')
            self._periodic_table_xml[language] = xml
        return self._periodic_table_xml[language]

    def supported_formats_xml(self, language):
        """Returns an XML document describing chemical formats
        supported by the chem_reader
        """
        doc = self._create_dom()
        root = doc.createElement("formats")
        doc.appendChild(root)
        to_sort = []
        for name,desc,exts in brailchem.chem_reader.ChemReader.known_format_descriptions():
            to_sort.append((name not in brailchem.chem_reader.ChemReader.important_formats,
                            desc, name, exts))
        to_sort.sort()
        for not_common,desc,name,exts in to_sort:
            elem = doc.createElement("format")
            common = not not_common
            if common:
                elem.setAttribute('common','True')
            if exts:
                elem.setAttribute('extensions', " ".join(exts))
            root.appendChild(elem)
            name_el = doc.createElement("name")
            name_el.appendChild(doc.createTextNode(name))
            elem.appendChild(name_el)
            desc_el = doc.createElement("description")
            desc_el.appendChild(doc.createTextNode(desc))
            elem.appendChild(desc_el)
        xml = doc.toxml()
        return xml
            
### HTTP output interface

class WebTree(twisted.web.resource.Resource):
    """Top-level web resource."""

    def __init__(self, service):
        twisted.web.resource.Resource.__init__(self)
        self._service = service
        self.putChild('smiles', SmilesWebResource(service))
        self.putChild('name', NameWebResource(service))
        self.putChild('periodic', PeriodicWebResource(service))
        self.putChild('chemfile', ChemFileWebResource(service))
        self.putChild('formats', FormatsWebResource(service))

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
    
    def render_POST(self, request):
        return self.render_GET(request)

class SmilesWebResource(XMLWebResource):
    """SMILES request web handler."""

    isLeaf = True

    _default_smiles = 'Oc1ccccc1C'

    def render_GET(self, request):
        if request.postpath:
            smiles = request.postpath[0]
        else:
            smiles = self._default_smiles
        language = request.args.get('language', ['en'])[0]
        defer = twisted.internet.defer.succeed(self._service.molecule_details_xml(smiles, "SMILES", language))
        defer.addCallback(self._cb_render_GET, request)
        return twisted.web.server.NOT_DONE_YET

class PeriodicWebResource(XMLWebResource):
    """Periodic table data."""
    
    isLeaf = True
        
    def render_GET(self, request):
        language = request.args.get('language', ['en'])[0]
        defer = twisted.internet.defer.succeed(self._service.periodic_table_xml(language))
        defer.addCallback(self._cb_render_GET, request)
        return twisted.web.server.NOT_DONE_YET

class NameWebResource(XMLWebResource):
    """Name request web handler."""

    isLeaf = True

    _default_name = 'benzene'

    def render_GET(self, request):
        if request.postpath:
            name = request.postpath[0]
        else:
            name = self._default_name
        language = request.args.get('language', ['en'])[0]
        defer = twisted.internet.defer.succeed(self._service.molecule_details_xml(name, "name", language))
        defer.addCallback(self._cb_render_GET, request)
        return twisted.web.server.NOT_DONE_YET

class ChemFileWebResource(XMLWebResource):
    """request web handler for chemical files."""

    isLeaf = True

    def render_POST(self, request):
        text = request.args.get('uploaded_file',[""])[0]
        format = request.args.get('format',['mol'])[0]
        language = request.args.get('language', ['en'])[0]
        defer = twisted.internet.defer.succeed(self._service.molecule_details_xml(text, format, language))
        defer.addCallback(self._cb_render_GET, request)
        return twisted.web.server.NOT_DONE_YET

class FormatsWebResource(XMLWebResource):
    """request web handler for chemical files."""

    isLeaf = True

    def render_GET(self, request):
        language = request.args.get('language', ['en'])[0]
        defer = twisted.internet.defer.succeed(self._service.supported_formats_xml(language))
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
