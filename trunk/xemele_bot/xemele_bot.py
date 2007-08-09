#!/usr/bin/python
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

import sys
import os
import xmpp
from config   import Config
from commands import Commands

class Bot:
  def __init__(self):
    self.buddylist = {}
    self.commands = Commands(self)


  def start(self):
    config         = Config()

    jid      = xmpp.JID(config['bot_jid'])
    user     = jid.getNode()
    server   = jid.getDomain()

    self.con = xmpp.Client(server, debug=[])
    conres = self.con.connect()
    if not conres:
        raise ("Unable to connect to server %s!" % server)
        sys.exit(1)
    if conres<>'tls':
        raise "Warning: unable to estabilish secure connection - TLS failed!"

    authres = self.con.auth(user, config['bot_password'], config['bot_resource'])

    if not authres:
        raise "Unable to authorize on %s - check login/password." % server
        sys.exit(1)
    if authres<>'sasl':
        raise ("Warning: unable to perform SASL auth os %s. Old " +
        "authentication method used!" % server)

    self.con.RegisterHandler('message',self.messageHandler)
    self.con.RegisterHandler('iq',self.rosterHandler, ns="jabber:iq:roster")
    self.con.sendInitPresence() # requestRoster=1

    #main loop
    while self.loop(): pass

  def getBuddyList(self):
    return self.buddylist

  def connection(self):
    return self.con

  def loop(self):
    try:
        self.con.Process(1)
    except KeyboardInterrupt: return False
    return True

  def rosterHandler(self, con, mess):
    """load the Bot's buddylist"""
    items = mess.getChildren()[0].getChildren()
    for item in items:
      if item.getAttr('subscription') == 'both':
        self.addBuddy(item.getAttr('jid'))
      else:
        if item.getAttr('subscription') == 'remove':
          self.removeBuddy(item.getAttr('jid'))

  def addBuddy(self, jid):
    if not jid in self.buddylist:# .has_kay(jid):
      self.buddylist[jid] = xmpp.JID(jid)

  def removeBuddy(self, jid):
    del self.buddylist[jid]

  def sendTo(self, to, msg):
    self.con.send(xmpp.Message(to, msg))

  def messageHandler(self, con, mess):
    msg    = mess.getBody().strip()
    sender = mess.getFrom()

    if ' ' in msg:
      command, args = msg.split(' ',1)
    else:
      command, args = msg, ''

    cmd = command.lower()

    if self.commands.supports(cmd):
      reply = self.commands.do(cmd, sender, args)
    else:
      reply = 'command not found: "%s". try "help"' % ( cmd, )

    if reply:
      self.sendTo(sender, reply)
# end #

print "bot started"
Bot().start()
print "bot killed"
