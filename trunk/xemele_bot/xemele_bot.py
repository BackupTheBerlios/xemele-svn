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
from config import Config
from commands import Commands

class Bot:
  def __init__(self):
    config = Config()

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

  def start(self):
    self.con.RegisterHandler('message',self.handler)
    self.con.sendInitPresence()
    while self.loop(): pass

  def loop(self):
    try:
        self.con.Process(1)
    except KeyboardInterrupt: return False
    return True

  def sendTo(self, to, msg):
    self.con.send(xmpp.Message(to, msg))

  def handler(self, con, mess):
    msg    = mess.getBody()
    sender = mess.getFrom()

    if ' ' in msg:
      command, args = msg.split(' ',1)
    else:
      command, args = msg, ''

    cmd = command.lower()

    objCommands = Commands()

    if objCommands.commands.has_key(cmd):
      reply = objCommands.commands[cmd](self.con, sender, args)
    else:
      reply = 'command not found: "%s". try "help"' % ( cmd, )

    if reply:
      self.sendTo(sender, reply)

  ### Helpers ###

  def assign(self, assigner, to, url):
    self.sendTo(jid, 'confirm_assign from=' + assigner + " atom=" + url)


  # end #

print "bot started"
Bot().start()
print "bot killed"

