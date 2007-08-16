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

import BaseHTTPServer
import codecs
import os
import urllib
import xml.sax.saxutils

from chem_server import ChemServer
from object_types import *

class DataProvider(object):

    def __init__ (self, *args, **kwargs):
        super(DataProvider, self).__init__(*args, **kwargs)
        self._server = ChemServer()

    def request_answer(self, request_path):
        data = self._ask_server(request_path)
        xml_data = self._transform_to_xml(data)
        return xml_data

    def _ask_server(self, request_path):
        server = self._server
        molecule = os.path.basename(urllib.unquote_plus(request_path)) or 'Oc1ccccc1C'
        session = server.connect()
        try:
            data = session.process_string(molecule, format="SMILES")
        finally:
            server.disconnect(session.number())
        return data

    def _transform_to_xml(self, data):
        def escape(text):
            return xml.sax.saxutils.escape(text)
        def attr_escape(text):
            return xml.sax.saxutils.quoteattr(text)            
        def transform(data, level=0):
            data_type = data.data_type()
            id = data.id()
            data_type_id = data_type.id()
            description = data_type.description()
            long_description = data_type.long_description()
            prefix = ' '*level
            contents = ''
            if isinstance(data, Value):
                contents += '%s<value>%s</value>\n' % (prefix, escape(unicode(data.value())),)
            if isinstance(data, Complex):
                contents += '%s<parts>\n' % (prefix,)
                for part in data.parts():
                    contents += transform(part.target(), level+1)
                contents += '%s</parts>\n' % (prefix,)
            if isinstance(data, Part):
                contents += '%s<neighbors>\n' % (prefix,)
                for neighbor in data.neighbors():
                    contents += '%s <link id="%s"/>\n' % (prefix, neighbor.target().id(),)
                contents += '%s</neighbors>\n' % (prefix,)
            if isinstance(data, MultiView):
                contents += '%s<views>\n' % (prefix,)
                for view in data.views():
                    contents += transform(view, level+1)
                contents += '%s</views>\n' % (prefix,)
            return ('%(prefix)s<data id=%(id)s type=%(data_type_id)s description=%(description)s long=%(long)s>\n%(contents)s%(prefix)s</data>\n' %
                    dict(prefix=prefix, id=attr_escape(unicode(id)), data_type_id=attr_escape(data_type_id),
                         description=attr_escape(description), long=attr_escape(long_description), contents=contents))
        return '<?xml version="1.0"?>\n' + transform(data)

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def __init__(self, *args, **kwargs):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
        self._data_provider = DataProvider()
    
    def do_GET(self):
        try:
            data_provider = self._data_provider
        except AttributeError:
            data_provider = self._data_provider = DataProvider()            
        xml_data = data_provider.request_answer(self.path)
        self.send_response(200)
        self.send_header('Content-type', 'application/xml')
        self.send_header('Content-Length', str(len(xml_data)))
        self.end_headers()
        self.wfile.write(codecs.getencoder('utf-8')(xml_data)[0])

def run():
    server = BaseHTTPServer.HTTPServer(('', 8000,), RequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    run()
