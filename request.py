import shlex

class Request(object):

  def __init__(self, fulluser, channel, msg, respond):
    self.fulluser = fulluser
    self.channel = channel
    self.message = msg
    self._respond = respond

  def respond(self, message):
    self._respond(self, message.encode('utf-8'))

  @property
  def args(self):
    return shlex.split(self.message)

  @property
  def nick(self):
    return self.fulluser.split('!')[0]

  @property
  def account(self):
    return self.fulluser.split('@', 1)[1]

  def __str__(self):
    return '<Request fulluser="%s" channel="%s" message="%s">' % (
        self.fulluser, self.channel, self.message)
