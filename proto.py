from twisted.words.protocols import irc

import jellyfish
import re

class BotProtocol(irc.IRCClient):

  def lineReceived(self, line):
    print line
    irc.IRCClient.lineReceived(self, line)
    self.factory.lines.append(line)

  def signedOn(self):
    for channel in self.factory.channels:
      self.join(channel)

  def respond_on_channel(self, request, msg):
    self.say(request.channel, '%s: %s' % (request.nick, msg))

  def respond_to_user(self, request, msg):
    self.msg(request.nick, msg)

  def privmsg(self, fulluser, channel, msg):
    if channel == self.nickname:
      respond = self.respond_to_user
    else:
      respond = self.respond_on_channel

    request = self.factory.request_factory(
        fulluser, channel, msg, respond, self)

    if msg[0] == self.factory.prefix:
      self.factory.handler.handle(request)
    else:
      self.factory.db.runQuery(
          'INSERT OR REPLACE INTO lasts (updated, user, channel, message) '
          'VALUES (datetime(), ?, ?, ?)', (fulluser, channel, msg))
      self.factory.db.runQuery(
          'INSERT OR REPLACE INTO lasts (updated, user, channel, message) '
          'VALUES (datetime(), ?, ?, ?)', (fulluser, channel, msg))

  def modeChanged(self, *args):
    self.log(args)

  def log(self, message):
    print message
