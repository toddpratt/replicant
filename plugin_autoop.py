import proto
import request

class JoinPlugin(object):

  def irc_JOIN(self, proto, fulluser, channels):
    req = request.Request(fulluser, channels[0], '', None, proto)
    print 'joined:', req.user
    print 'auto-op:', proto.factory.conf['plugins']['auto-op']
    if req.user in proto.factory.conf['plugins']['auto-op']:
      print 'opping'
      proto.mode(channels[0], True, 'o', user=req.nick)

def register():
  proto.BotProtocol.register_plugin(JoinPlugin)
