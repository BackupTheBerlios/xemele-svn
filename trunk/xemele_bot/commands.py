##
#   Copyright (C) 2007 by Marcelo Jorge Vieira (metal) <metal@alucinados.com>
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

import inspect
import re
import xmpp
from tag           import *
from jid_extension import *
from content       import *


class Commands:

  cmd_prefix = 'cmd_'

  def __init__(self, bot):
    self.bot = bot
    self.commands = {}

    for (method, value) in inspect.getmembers(self):
      if callable(getattr(self, method)) and method.startswith('cmd_'):
        self.commands[method[len(self.cmd_prefix):]] = value

  def supports(self, cmd):
    return self.commands.has_key(cmd)

  def do(self, cmd, sender, args):
    return self.commands[cmd](sender, args)


  ##### Commands #######

  def cmd_help(self, sender, args):
    return "go to hell!"

  def cmd_alfred(self, sender, args):
    return "Yes, master Bruce?"

  def cmd_visible(selfsender, args):
    if args == 'on':
      self.bot.connection().sendPresence(jid=sender, typ='available')
      return "Visibility Enabled!"
    elif args == 'off':
      self.bot.connection().sendPresence(jid=sender, typ='unavailable')
      return "Visibility Disabled!"

  def cmd_assign(self, sender, msg):
    """Used to assign an atom URL to a JID. This
       command sends a confirmation request to the assignee
       asking for approval.
       Syntax: assign to="<jid@server>" atom="<http://....>"

       Prototype usage:
          #foo associates content to user bar
          foo says to bot: assign to="bar@server" atom="http://test.com"

          #bot requests aproval
          bot says to bar: confirm_assign from="foo@server" atom="http://test.com"

          #bar confirms
          bar says to bot: confirm_assign from="foo@server" atom="http://test.com"

          #bot confirms association
          bot says to foo:  assigned!

          Now we can query data:
          someone says to bot: query_contents for="bar@server"
          bot says to someone: 0: http://test
       """

    res = re.search('to="([^"]+)"\s+atom="([^"]+)"', msg)
    if not res:
      return ('Error! cmd syntax: ' +
          'assign to="<somejid@server>" atom="<http://someurl>"')

    self.requestConfirmation(sender.getStripped(), res.group(1), res.group(2))

  def cmd_confirm_assign(self, sender, msg):
    """Used to confirm and persist the subscription
       made previously, in the database. This is the
       command the bot sends to the assignee. If he/she
       replies the exact copy of the command, that is
       the confirmation"""

    res = re.search('from="([^"]+)"\s+atom="([^"]+)"', msg)
    if not res:
      return ('Error! cmd syntax: ' +
          'confirm_assign from="<somejid@server>" atom="<http://someurl>"')

    self.assign(sender.getStripped(), res.group(1), res.group(2))

  def cmd_query_contents(self, sender, msg):
    res = re.search('for="([^"]*)', msg)
    if not res:
      return ('Error: cmd syntax: ' +
          'query_contents for="<somejid@server>"')

    return self.queryContents(sender.getStripped(), res.group(1))


  ### Helpers ###

  def requestConfirmation(self, assigner, to, url):
    self.bot.sendTo(to, 'confirm_assign from="' + assigner + '" atom="' + url + '"')

  def assign(self, to, assigner, url):
    #jid_assigner = xmpp.JD(assigner)
    jid_to = self.bot.getBuddyList()[to]
    c = Content(url)
    jid_to.addContent(c)
    self.bot.sendTo(assigner, 'assigned!') #TODO: send contents update

  def queryContents(self, sender, who):
    jid = self.bot.getBuddyList()[who]

    msg = ''
    idx = 1
    for item in jid.getContents():
      msg += str(idx) + ":" + item.getData() + "\n"
      idx += 1
    return msg
