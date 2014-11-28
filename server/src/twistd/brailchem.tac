# -*- python -*-
# Copyright (C) 2007, 2014 Brailcom, o.p.s.
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

import twisted.application.internet
import twisted.application.service
import twisted.web.server
import brailchem.twistd.server

application = twisted.application.service.Application('brailchem')

web_tree = brailchem.twistd.server.WebTree(brailchem.twistd.server.ChemInterface())
service = twisted.application.internet.TCPServer(8000, twisted.web.server.Site(web_tree))
service.setServiceParent(application)
