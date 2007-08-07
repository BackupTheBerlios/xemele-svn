#!/usr/bin/python

import sys
import os
import xmpp

BOT_JID  = 'foo@server'
BOT_PASS = '12345'

class Bot:
  def __init__(self):
    jid      = xmpp.JID(BOT_JID )
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
        raise "Warning: unable to perform SASL auth os %s. Old authentication method used!" % server

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
    text = mess.getBody()
    sender = mess.getFrom()

    self.cmdHelloWorld(sender)

  def cmdHelloWorld(self, sender):
    self.con.send(xmpp.Message(sender, "Yes, master"))


Bot().start()

