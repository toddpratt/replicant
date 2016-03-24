import collections
import command
import plugin_base
import proto
import request


class JoinPlugin(object):

  def __init__(self, catalog):
    self._catalog = catalog

  def irc_JOIN(self, proto, fulluser, channels):
    req = request.Request(fulluser, channels[0], '', None, proto,
            proto.factory.ircnet)
    messages = self._catalog.get("tells").get(req.nick, [])
    for message in messages:
      req.respond(message)
    try:
      del self._catalog.get("tells")[req.nick]
    except KeyError:
      pass


class TellCommand(plugin_base.BaseCommand):

  def handle_user(self, req):
    _, nicks, msg = req.message.split(None, 2)
    nicks = nicks.split(',')
    for nick in nicks:
      self._catalog.get("tells").setdefault(nick, [])
      self._catalog.get("tells")[nick].append(msg)
    req.respond("will do")

class ShowUsersCommand(plugin_base.BaseCommand):

  def handle_user(self, req):
    req.respond(", ".join(self._catalog.get("tells").iterkeys()))

def register(catalog):
  command.CommandHandler.register('tell', TellCommand(catalog))
  command.CommandHandler.register('tells', ShowUsersCommand(catalog))
  proto.BotProtocol.register_plugin(JoinPlugin(catalog))
