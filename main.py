from twisted.enterprise import adbapi 
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.internet import ssl
from twisted.protocols import basic
from twisted.words.protocols import irc

import datetime
import re
import shlex
import sys

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

class IRCBot(irc.IRCClient):

  def lineReceived(self, line):
    irc.IRCClient.lineReceived(self, line)
    self.lines.append(line)

  def signedOn(self):
    for channel in self.channels:
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

    request = Request(fulluser, channel, msg, respond)
    if msg[0] == self.prefix:
      try:
        function_name = 'do_' + request.args[0][1:]
      except ValueError:
        pass
      else:
        try:
          function = getattr(self, function_name)
        except AttributeError:
          pass
        else:
          function(request)
    else:
      self.db.runQuery(
          'INSERT OR REPLACE INTO lasts '
          '(updated, user, channel, message) '
          'VALUES (datetime(), ?, ?, ?)',
          (fulluser, channel, msg))

  def do_last(self, request):
    if request.account in self.users:
      d = self.db.runQuery('SELECT updated, channel, user, message '
                      'FROM lasts WHERE user LIKE ?',
          (request.args[1] + '!%', ))
      d.addCallback(self.reportLast, request)
      d.addErrback(self.reportError, request)
    else:
      d = self.db.runQuery('SELECT updated, channel, user, message '
                      'FROM lasts WHERE user LIKE ? AND channel = ?',
          (request.args[1] + '!%', request.channel))
      d.addCallback(self.reportLast, request)

  def reportLast(self, result, request):
    request.respond('%s %s %s "%s"' % result[0])

  def do_ping(self, request):
    if request.account in self.users:
      request.respond('I am your servant.')
    else:
      request.respond('pong')

  def reportError(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())

  def reportSuccess(self, result, request):
    self.last_result = result
    self.iter_result = iter(result)
    request.respond('OK: %d' % len(result))

  def do_restart(self, request):
    if request.account in self.users:
      self.iter_result = iter(self.last_result)

  def do_count(self, request):
    if request.account in self.users:
      d = self.db.runQuery('SELECT COUNT(*) FROM log')
      d.addCallback(self.reportCount, request)
      d.addErrback(self.reportError, request)

  def reportCount(self, result, request):
    request.respond('the log has %d entries' % result[0][0])

  def do_next(self, request):
    try:
      request.respond(str(next(self.iter_result)))
    except StopIteration:
      request.respond('ain\'t no more')

  def do_query(self, request):
    if request.account in self.users:
      query = request.message.split(None, 1)[1]
      d = self.db.runQuery(query)
      d.addCallback(self.reportSuccess, request)
      d.addErrback(self.reportError, request)

  def do_aa(self, request):
    if request.account in self.users:
      for account in request.args[1:]:
        self.users.add(account)

  def do_say(self, request):
    if request.account in self.users:
      self.say(request.args[1], ' '.join(request.args[2:]))

  def do_report(self, request):
    if request.account in self.users:
      request.respond('"%s" has been reported to the NSA.' % request.args[1])

  def do_known(self, request):
    d = self.db.runQuery('SELECT user FROM lasts')
    d.addErrback(self.reportSuccess, request)
    d.addErrback(self.reportError, request)

  def do_grep(self, request):
    if request.account in self.users:
      regexes = [re.compile(p) for p in request.args[1:]]
      self.last_result = []
      for line in self.lines:
        if any(p.search(line) for p in regexes):
          self.last_result.append(line)
      self.iter_result = iter(self.last_result)
      request.respond('%d matches' % len(self.last_result))

  def modeChanged(self, *args):
    self.log(args)

  def log(self, message):
    print message

class BotFactory(protocol.ClientFactory):

  reconnect = None

  def buildProtocol(self, addr):
    self.ircbot = proto = IRCBot()
    proto.factory = self
    proto.nickname = "replicant"
    proto.realname = "Roy Batty"
    proto.password = None
    proto.username = proto.nickname
    proto.channels = self.channels
    proto.lines = self.lines = []
    proto.users = self.users
    proto.prefix = '@'
    proto.db = self.db
    proto.last_result = tuple()
    proto.iter_result = iter(tuple())
    return self.ircbot

  def clientConnectionLost(self, connector, failure):
    print failure.getErrorMessage()
    if self.reconnect is None:
      self.reconnect = 0
    elif self.reconnect < 20:
      self.reconnect += 5
    reactor.callLater(self.reconnect, connector.connect)


class UserDB(object):

  def __init__(self, db):
    self.db = db
    self.ready = False
    self.load_from_table()

  def add(self, account):
    self.users.add(account)
    d.self.db.runQuery(
        'INSERT OR REPLACE INTO admins (account) VALUES (?)', account)

  def load_from_table(self):
    d = self.db.runQuery('SELECT account FROM admins')
    d.addCallback(self.gotAdminAccounts)
    d.addErrback(self.gotError)

  def gotError(self, *args):
    print args

  def gotAdminAccounts(self, results):
    self.users = set(row[0] for row in results)
    self.ready = True

  def __contains__(self, item):
    if self.ready:
      return item in self.users
    else:
      raise ValueError('admin users list hasn\'t loaded yet.')


if __name__ == "__main__":
  dbpool = adbapi.ConnectionPool('sqlite3', 'db.sqlite3')
  f = BotFactory()
  f.db = dbpool
  f.channels = { "#nerdism" }
  f.irc_servername = 'Chicago.IL.US.Undernet.Org'
  f.users = UserDB(dbpool)
  f.master = 'sucralose'

  port = 6669
  reactor.connectTCP(f.irc_servername, port, f)
  reactor.run()
