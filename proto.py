from twisted.words.protocols import irc

class BotProtocol(irc.IRCClient):
  plugins = []

  def sendLine(self, line):
    self.transport.write(line.encode('utf-8') + '\r\n')

  def lineReceived(self, line):
    irc.IRCClient.lineReceived(self, line)
    print line

  @classmethod
  def reset_plugins(cls):
    cls.plugins = []

  @classmethod
  def register_plugin(cls, plugin):
    cls.plugins.append(plugin)

  def signedOn(self):
    for channel in self.factory.channels:
      self.join(channel)

  def respond_on_channel(self, request, msg):
    self.say(request.channel, '%s: %s' % (request.nick, msg))

  def respond_to_user(self, request, msg):
    self.msg(request.nick, msg)

  def privmsg(self, fulluser, channel, msg):
    if msg[0] == self.factory.prefix:
      if channel == self.nickname:
        respond = self.respond_to_user
      else:
        respond = self.respond_on_channel
      request = self.factory.request_factory(
          fulluser, channel, msg, respond, self, self.factory.ircnet)
      self.factory.handler.handle(request)
    self.private_message(fulluser, channel, msg)

  def call_plugins(name):
    def wrapper(*args, **kwargs):
      for plugin in BotProtocol.plugins:
        method = getattr(plugin, name, None)
        if method:
          method(*args, **kwargs)
    return wrapper

  irc_JOIN = call_plugins('irc_JOIN')
  irc_PART = call_plugins('irc_PART')
  irc_QUIT = call_plugins('irc_QUIT')
  irc_MODE = call_plugins('irc_MODE')
  irc_PING = call_plugins('irc_PING')
  irc_PRIVMSG = call_plugins('irc_PRIVMSG')
  irc_NOTICE = call_plugins('irc_NOTICE')
  irc_NICK = call_plugins('irc_NICK')
  irc_KICK = call_plugins('irc_KICK')
  irc_TOPIC = call_plugins('irc_TOPIC')
  private_message = call_plugins('privmsg')
