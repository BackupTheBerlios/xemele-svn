#!/usr/bin/python

## vim:
#
# :set shiftwidth=2 "using 2 spaces for identation"
# :set tabstop=2    "two spaces per tab"
# :set expandtab    "using tabs as spaces"
# :retab            "convert existing tabs to spaces"


## Adding commands to the BOT
#
# simply define a method starting with 'cmd_'
#    example: def cmd_say_hi(self, sender, message):
#
# The above method will be called whenever someone sends a message 'say_hi'
#

import sys
import os
import xmpp
import re

BOT_JID  = 'foo@server'
BOT_PASS = '12345'

class Bot:
  def __init__(self):
    jid      = xmpp.JID(BOT_JID)
    user     = jid.getNode()
    server   = jid.getDomain()

    self.con = xmpp.Client(server, debug=[])

    conres = self.con.connect()
    if not conres:
        raise ("Unable to connect to server %s!" % server)
        sys.exit(1)
    if conres<>'tls':
        raise "Warning: unable to estabilish secure connection - TLS failed!"

    authres = self.con.auth(user,BOT_PASS)

    if not authres:
        raise "Unable to authorize on %s - check login/password." % server
        sys.exit(1)
    if authres<>'sasl':
        raise ("Warning: unable to perform SASL auth os %s. Old " + 
        "authentication method used!" % server)

  def start(self):
    self.con.RegisterHandler('message',self.handler)
    self.con.sendInitPresence()
    while self.loop(): pass

  def loop(self):
    try:
        self.con.Process(1)
    except KeyboardInterrupt: return False
    return True

  def handler(self, con, mess):
    msg    = mess.getBody()
    sender = mess.getFrom()

    if len(msg) == 0: return

    cmd = msg.split()[0]

    for method in self.commandMethods():
      if method.startswith('cmd_') and method[4:] == cmd:
        getattr(self, method)(sender, msg)

  def commandMethods(self):
    return [method for method in dir(self) if 
        callable(getattr(self, method)) and method.startswith('cmd_')]


  def sendTo(self, to, msg):
    self.con.send(xmpp.Message(to, msg))


  ### Commands ###

  def cmd_alfred(self, sender, msg):
    self.sendTo(sender, "Yes, master")

  def cmd_assign(self, sender, msg):
    """Used to assign an atom URL to a JID. This
       command sends a confirmation request to the assignee
       asking for approval.
       Syntax: assign to="jid@server" atom="http://...." """

    res = re.search('assign\s+to="([^"]+)"\s+atom="([^"]+)"', msg)
    if not res:
      self.sendTo(sender, 'Error! cmd syntax: ' + 
          'assign to="<somejid@server>" atom="<someurl>"')
      return

    self.assign(res.group(1), res.group(2))
    self.sendTo(sender, )
    #assign atom="http://..." to="jid@server"

  def cmd_confirm(self, sender, msg):
    """Used to confirm and persist the subscription 
       made previously in the database."""

    #Syntax: confirm from="subscriber@server" atom="http://...."

  ### Helpers ###

  def assign(self, assigner, to, url):
    self.sendTo(jid, 'confirm_assign from=' + assigner + " atom=" + url)


  # end #

Bot().start()

