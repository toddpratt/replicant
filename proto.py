from twisted.words.protocols import irc

class BotProtocol(irc.IRCClient):
  plugins = []

  def lineReceived(self, line):
    irc.IRCClient.lineReceived(self, line)
    print line

  @classmethod
  def register_plugin(cls, plugin):
    cls.plugins.append(plugin())

  def signedOn(self):
    for channel in self.factory.channels:
      self.join(channel)

  def respond_on_channel(self, request, msg):
    self.say(request.channel, '%s: %s' % (request.nick, msg))

  def respond_to_user(self, request, msg):
    self.msg(request.nick, msg)

  def privmsg(self, fulluser, channel, msg):
    print 'privmsg called:', fulluser, channel, msg
    if msg[0] == self.factory.prefix:
      if channel == self.nickname:
        respond = self.respond_to_user
      else:
        respond = self.respond_on_channel
      request = self.factory.request_factory(
          fulluser, channel, msg, respond, self)
      self.factory.handler.handle(request)

    #self.dispatch(self.get_methods('privmsg'), fulluser, channel, msg)

  def dispatch(self, methods, *args, **kwargs):
    print 'dispatch:', methods, args, kwargs
    for method in methods:
      method(*args, **kwargs)

  def call_plugins(name):
    def wrapper(*args, **kwargs):
      for plugin in BotProtocol.plugins:
        method = getattr(plugin, name)
        if method:
          method(*args, **kwargs)
    return wrapper

  irc_JOIN = call_plugins('irc_JOIN')
