import shlex

class Request(object):

  def __init__(self, fulluser, channel, msg, respond, proto, chatnet):
    self.fulluser = fulluser
    self.channel = channel
    self.message = msg
    if respond:
      self._respond = respond
    else:
      self._respond = self.default_respond
    self.proto = proto
    self.chatnet = chatnet

  def respond(self, message):
    self._respond(self, message)

  def say(self, channel, message):
    self.proto.say(channel, message)

  def default_respond(self, message):
    self.say("%s: %s" % (self.nick, message))

  @property
  def args(self):
    return shlex.split(self.message)

  @property
  def nick(self):
    return self.fulluser.split('!')[0]

  @property
  def user(self):
    return self.fulluser.split('!')[1]

  @property
  def account(self):
    return self.fulluser.split('@', 1)[1]

  def for_reply(self, fulluser):
    return Request(fulluser, self.channel, '', self._respond, self.proto,
            self.chatnet)
