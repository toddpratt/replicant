import proto
import request

class JoinPlugin(object):

  def irc_JOIN(self, proto, fulluser, channels):
    req = request.Request(fulluser, channels[0], '', None, proto)
    if req.user in proto.factory.conf['plugins']['auto-op']:
      proto.mode(channels[0], True, 'o', user=req.nick)

def register(catalog):
  proto.BotProtocol.register_plugin(JoinPlugin)
