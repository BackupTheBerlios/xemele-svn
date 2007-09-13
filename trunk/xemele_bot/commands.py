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

  def cmd_associate(self, sender, msg):
    """
    Use it to associate an user JID to a pair:
           application JID     - the JID of the xemele-enabled application
           application user id - the ID that represents the user in that application

    Example:
      associate user-JID="romeo@example.org" application-JID="orkut@jabber.org" user-id="romeo"
    """

    res = re.search('\s*user-JID="([^"]+)"\s+application-JID="([^"]+)"\s+user-id="([^"]+)"\s*', msg)
    if not res:
      return ('Error! cmd syntax: ' +
          'associate user-JID="<user@server>" application-JID="<app@server>" user-id="<userid>"')

    self.associate(res.group(1), res.group(2), res.group(3))
    return "Done association!"

  def cmd_query_user(self, sender, msg):
    """
        query_user jid="romeo@example.org"
    """

    res = re.search('\s*jid="([^"]+)"\s*', msg)
    if not res:
      return ('Error! cmd syntax: ' +
          'query_user jid="<user@server>"')

    return self.query_user(res.group(1))

  #def cmd_confirm_assign(self, sender, msg):
    #"""Used to confirm and persist the subscription
       #made previously, in the database. This is the
       #command the bot sends to the assignee. If he/she
       #replies the exact copy of the command, that is
       #the confirmation"""

    #res = re.search('from="([^"]+)"\s+atom="([^"]+)"', msg)
    #if not res:
      #return ('Error! cmd syntax: ' +
          #'confirm_assign from="<somejid@server>" atom="<http://someurl>"')

    #self.assign(sender.getStripped(), res.group(1), res.group(2))

  #def cmd_query_contents(self, sender, msg):
    #res = re.search('for="([^"]*)', msg)
    #if not res:
      #return ('Error: cmd syntax: ' +
          #'query_contents for="<somejid@server>"')

    #return self.queryContents(sender.getStripped(), res.group(1))


  ### Helpers ###

  def associate(self, userJID, appJID, userid):
    self.bot.getDB().cursor().execute(
        "INSERT INTO associations (user_jid, app_jid, app_userid) VALUES (%s,%s,%s)",
        (userJID, appJID, userid))


  def query_user(self, userJID):
    cursor = self.bot.getDB().cursor()
    cursor.execute(
      "SELECT app_jid, app_userid FROM associations WHERE user_jid = %s", userJID)

    ret = ""
    for x in cursor.fetchall():
      ret += x[0] + ":" + x[1] + "\n"
    return ret

    #jid_to = self.bot.getBuddyList()[to]
    #c = Content(url)
    #jid_to.addContent(c)
    #self.bot.sendTo(assigner, 'assigned!') #TODO: send contents update

  #def queryContents(self, sender, who):
    #jid = self.bot.getBuddyList()[who]

    #msg = ''
    #idx = 1
    #for item in jid.getContents():
      #msg += str(idx) + ":" + item.getData() + "\n"
      #idx += 1
    #return msg
