import proto
import request

class JoinPlugin(object):

  def __init__(self, catalog):
    self._catalog = catalog

  def irc_JOIN(self, proto, fulluser, channels):
    req = request.Request(fulluser, channels[0], '', None, proto,
            proto.factory.ircnet)
    config = self._catalog.config["servers"][req.chatnet]
    users = config["channels"][req.channel]["operators"]
    if req.user in users:
      proto.mode(channels[0], True, 'o', user=req.nick)

def register(catalog):
  proto.BotProtocol.register_plugin(JoinPlugin(catalog))
