class CommandHandler(object):

  def __init__(self, db, users, lines, conf):
    self.db = db
    self.users = users
    self.lines = lines

  def handle(self, request):
    try:
      function_name = 'do_' + request.args[0][1:]
    except ValueError:
      pass
    else:
      getattr(self, function_name, lambda _: None)(request)

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
