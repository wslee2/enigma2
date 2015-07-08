# IsNet Converter
# Copyright (c) 2boom 2014
# v.0.1-r0
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from Components.Converter.Converter import Converter
from Components.Element import cached
from Poll import Poll
import socket


class IsNet(Poll, Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		Poll.__init__(self)
		self.poll_interval = 3000
		self.poll_enabled = True

	@cached
	def getBoolean(self):
		try:
			socket.gethostbyaddr('www.google.com')
		except:
			return False
		return True
		
	boolean = property(getBoolean)

	def changed(self, what):
		if what[0] is self.CHANGED_SPECIFIC:
			Converter.changed(self, what)
		elif what[0] is self.CHANGED_POLL:
			self.downstream_elements.changed(what)
