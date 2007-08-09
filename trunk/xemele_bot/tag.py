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

class TagNotFound: pass


# Class for Tags associated with JID
# use tag.tagData(something) to make associations,
# tag.save() to commit it
class Tag:
  def __init__(self, name, jid):
    self.name = name
    self.jid  = jid
    self.taggedData = []

  def setName(self, name):
    self.name = name

  def getName(self):
    return self.name

  def setJID(self,jid):
    self.jid = jid

  def getJID(self):
    return self.jid

  def tagData(self, data):
    self.taggedData.append(data)

  def save(self):
    self.jid.addUniqueTag(self)

# Class for collection of Tags (Duh!).
# Simplify using many tags to tag a single content:
# tagCollection.tagData(data)

class TagCollection:
  def __init__(self, jid, strtags = None):
    """strtags: a string with tags separated by ','"""
    self.jid = jid
    self.collection = []

    if strtags != None:
      for item in [s.strip() for s in strtags.split(',')]:
        self.collection.append(Tag(item, jid))

  def exists(self, name):
    """Check if a tag with given name exists in the collection"""
    try:
      self.get(name)
    except TagNotFound:
      return False
    return True

  def get(self, name):
    """returns a tag object given its name"""
    for item in self.collection:
      if item.getName() == name:
        return item
    raise TagNotFound()

  def getAll(self):
    """return the list of tag objects"""
    return self.collection

  def tagData(self, data):
    """associate the data with all tags represented by this collection"""
    for item in self.collection:
      item.tagData(data)

  def append(self, tag):
    self.collection.append(tag)


  def save(self):
    for item in self.collection:
      item.save()

  def __iter__(self):
    return iter(self.collection)


######### end #########

#some irrelevant tests
if __name__ == '__main__':
  jid = xmpp.JID('bot@test')
  tags = jid.tagsFor('other, stuff')
  for item in tags:
    j = item.getJID()
    print item.getName() + ' ' + item.getJID().getStripped()


  print j.getTags().getAll()

  tags.save()

  for item in j.getTags().getAll():
    print 'saved ' + item.getName()

