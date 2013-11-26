import command

class BaseCommand(object):

  def handle(self, request):
    if request.account in request.users:
      self.handle_admin(request)
    else:
      self.handle_user(request)

  def handle_admin(self, request):
    raise NotImplementedError('override handle_admin')

  def handle_user(self, request):
    request.respond('You need to be an administrator for that command.')

class DatabaseCommand(BaseCommand):

  def __init__(self, query):
    self.query = query

  def handle_admin(self, request):
    self.handle_query(request)

  def handle_query(self, request):
    d = request.db.runQuery(self.query)
    d.addCallback

  def reportSuccess(self, result, request):
    request.results.append(result)
    request.respond('OK: rows=%d' % len(result))

  def report_error(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())

class PingCommand(BaseCommand):

  def handle_admin(self, request):
    request.respond('I am your servent.')

  def handle_user(self, request):
    request.respond('pong.')

command.CommandHandler.register('ping', PingCommand())
command.CommandHandler.register(
    'count', DatabaseCommand('SELECT COUNT(*) FROM lasts'))

