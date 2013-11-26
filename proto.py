from twisted.words.protocols import irc

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

    request = self.factory.request_factory(fulluser, channel, msg, respond)
    if msg[0] == self.factory.prefix:
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
      self.factory.db.runQuery(
          'INSERT OR REPLACE INTO lasts '
          '(updated, user, channel, message) '
          'VALUES (datetime(), ?, ?, ?)',
          (fulluser, channel, msg))

  def do_last(self, request):
    if request.account in self.factory.users:
      d = self.factory.db.runQuery('SELECT updated, channel, user, message '
                      'FROM lasts WHERE user LIKE ?',
          (request.args[1] + '!%', ))
      d.addCallback(self.reportLast, request)
      d.addErrback(self.reportError, request)
    else:
      d = self.factory.db.runQuery('SELECT updated, channel, user, message '
                      'FROM lasts WHERE user LIKE ? AND channel = ?',
          (request.args[1] + '!%', request.channel))
      d.addCallback(self.reportLast, request)

  def reportLast(self, result, request):
    request.respond('%s %s %s "%s"' % result[0])

  def do_ping(self, request):
    if request.account in self.factory.users:
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
    if request.account in self.factory.users:
      self.iter_result = iter(self.last_result)

  def do_count(self, request):
    if request.account in self.factory.users:
      d = self.factory.db.runQuery('SELECT COUNT(*) FROM log')
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
    if request.account in self.factory.users:
      query = request.message.split(None, 1)[1]
      d = self.factory.db.runQuery(query)
      d.addCallback(self.reportSuccess, request)
      d.addErrback(self.reportError, request)

  def do_aa(self, request):
    if request.account in self.factory.users:
      for account in request.args[1:]:
        self.factory.users.add(account)

  def do_say(self, request):
    if request.account in self.factory.users:
      self.say(request.args[1], ' '.join(request.args[2:]))

  def do_report(self, request):
    if request.account in self.factory.users:
      request.respond('"%s" has been reported to the NSA.' % request.args[1])

  def do_known(self, request):
    d = self.factory.db.runQuery('SELECT user FROM lasts')
    d.addErrback(self.reportSuccess, request)
    d.addErrback(self.reportError, request)

  def do_grep(self, request):
    if request.account in self.factory.users:
      regexes = [re.compile(p) for p in request.args[1:]]
      self.last_result = []
      for line in self.factory.lines:
        if any(p.search(line) for p in regexes):
          self.last_result.append(line)
      self.iter_result = iter(self.last_result)
      request.respond('%d matches' % len(self.last_result))

  def modeChanged(self, *args):
    self.log(args)

  def log(self, message):
    print message
