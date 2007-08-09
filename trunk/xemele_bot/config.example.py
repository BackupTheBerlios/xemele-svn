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

class Config(dict):

  def __init__(self):
    self['bot_jid']      = 'jid@jabber-br.org'
    self['bot_password'] = 'pass'
    self['bot_resource'] = 'xemele'
    self['bot_owner']    = 'metal'
