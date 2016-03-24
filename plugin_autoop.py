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
    if self._catalog.is_operator(req.chatnet, req.channel, req.account):
      proto.mode(channels[0], True, 'o', user=req.nick)


class CheckOpMatchCommand(plugin_base.BaseCommand):

  def handle_user(self, req):
    if self._catalog.is_operator(req.chatnet, req.channel, req.account):
      req.respond('you are an operator')
    else:
      req.respond('you are not an operator -- maybe authenticate to services?')


class AddOpCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, req):
    self._catalog.get_channel_config(req.chatnet, req.channel)["operators"].append(req.args[1])


def register(catalog):
  proto.BotProtocol.register_plugin(JoinPlugin(catalog))
  command.CommandHandler.register('opadd', AddOpCommand(catalog))
  command.CommandHandler.register('opcheck', CheckOpMatchCommand(catalog))
