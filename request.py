import shlex

class Request(object):

  def __init__(self, fulluser, channel, msg, respond, proto):
    self.fulluser = fulluser
    self.channel = channel
    self.message = msg
    self._respond = respond
    self.proto = proto

  def respond(self, message):
    self._respond(self, message.encode('utf-8'))

  def say(self, channel, message):
    self.proto.say(channel, message)

  @property
  def args(self):
    return shlex.split(self.message)

  @property
  def nick(self):
    return self.fulluser.split('!')[0]

  @property
  def account(self):
    return self.fulluser.split('@', 1)[1]

  def for_reply(self, fulluser):
    return Request(fulluser, self.channel, '', self._respond, self.proto)
