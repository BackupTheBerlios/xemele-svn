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
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#
# Public License can be found at http://www.gnu.org/copyleft/lgpl.html
##

import sys
import os
import xmpp
import MySQLdb
from config   import Config
from commands import Commands

class Bot:
  def __init__(self):
    self.buddylist = {}
    self.commands = Commands(self)


  def start(self):
    self.config = Config()
    self.init_db()
    self.start_bot()

  def init_db(self):
    self.debug("- Initializing DB connection...")
    self.dbcon = MySQLdb.connect (host   = self.config['db_host'],
                                  user   = self.config['db_user'],
                                  passwd = self.config['db_pass'],
                                  db     = self.config['db_name'])

    self.debug("DONE!")
    #cursor = conn.cursor ()
    #cursor.execute ("SELECT VERSION()")
    #row = cursor.fetchone ()
    #print "server version:", row[0]
    #cursor.close ()
    #conn.close ()

  def start_bot(self):
    self.debug("- Initializing Jabber connection...")

    jid      = xmpp.JID(self.config['bot_jid'])
    user     = jid.getNode()
    server   = jid.getDomain()

    self.con = xmpp.Client(server, debug=[])
    conres = self.con.connect()
    if not conres:
        raise ("Unable to connect to server %s!" % server)
        sys.exit(1)
    if conres<>'tls':
        raise "Warning: unable to estabilish secure connection - TLS failed!"

    self.debug("Connected!")
    self.debug("- Authenticating...")

    authres = self.con.auth(user, self.config['bot_password'], self.config['bot_resource'])

    if not authres:
        raise "Authentication failure on %s -- check bot's login/password." % server
        sys.exit(1)
    if authres<>'sasl':
        raise ("Warning: unable to perform SASL auth os %s. Old " +
        "authentication method used!" % server)

    self.debug("DONE!")

    self.con.RegisterHandler('message',self.messageHandler)
    self.con.RegisterHandler('iq',self.rosterHandler, ns="jabber:iq:roster")
    self.con.sendInitPresence() # requestRoster=1

    self.debug("- Entering main loop...")
    while self.loop(): pass

  def getBuddyList(self):
    return self.buddylist

  def getDB(self):
    return self.dbcon

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

  def debug(self, msg):
    print msg
# end #

print "bot started"
Bot().start()
print "bot killed"
