from twisted.words.protocols import irc

class BotProtocol(irc.IRCClient):
  plugins = []

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

    self.dispatch(self.get_methods('privmsg'), fulluser, channel, msg)

  def dispatch(self, methods, *args, **kwargs):
    print 'dispatch:', methods, args, kwargs
    for method in methods:
      method(*args, **kwargs)

  def get_methods(self, name):
    methods = []
    for plugin in self.plugins:
      obj = getattr(plugin, name, None)
      if callable(obj):
        methods.append(obj)
    return methods

  def __getattr__(self, name):
    methods = self.get_methods(name)
    if not methods:
      raise AttributeError('%s: no such attribute' % name)
    def dispatch(*args, **kwargs):
      self.dispatch(methods, *args, **kwargs)
    return dispatch
