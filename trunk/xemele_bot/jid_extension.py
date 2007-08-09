##
#   Copyright (C) 2007 by Thiago Silva <tsilva@sourcecraft.info>
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# Public License can be found at http://www.gnu.org/copyleft/lgpl.html
##
import xmpp
from   tag import *

class JIDMixin:
  def __init__(self, *args):
    self.base_init(*args)
    self.tags = TagCollection(self)
    self.contents = []

  def addContent(self, c):
    self.contents.append(c)

  def getContents(self):
    return self.contents

  def tagFor(self, tagname):
    if not self.tags.exists(tagname):
      tag = Tag(tagname, self)
    else:
      tag = self.tags.get(tagname)
    return tag

  def tagsFor(self, taglist):
    """from a string of tags "blog, stuff, etc"
       create a TagCollection associated to myself
       and return it"""

    ret = TagCollection(self)

    for item in [s.strip() for s in taglist.split(',')]:
      if self.tags.exists(item):
        ret.append(self.tags.get(item))
      else:
        ret.append(Tag(item, self))

    return ret

  def getTags(self):
    return self.tags

  def addUniqueTag(self, tag):
    found = False
    for item in self.tags:
      if item.getName() == tag.getName():
        found = True

    if not found:
      self.tags.append(tag)


xmpp.JID.base_init = xmpp.JID.__init__
del xmpp.JID.__init__
xmpp.JID.__bases__ += (JIDMixin,)
