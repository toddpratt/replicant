import command
import web

class BaseCommand(object):

  def handle(self, request):
    if request.account in request.users:
      self.handle_admin(request)
    else:
      self.handle_user(request)

  def handle_admin(self, request):
    self.handle_user(request)

  def handle_user(self, request):
    raise NotImplementedError('override handle_admin')

class BaseAdminCommand(BaseCommand):

  def handle_admin(self, request):
    raise NotImplementedError('override handle_admin')

  def handle_user(self, request):
    request.respond('You need to be an administrator for that command.')

class DatabaseCommand(BaseAdminCommand):

  def __init__(self, query):
    self.query = query

  def handle_admin(self, request):
    self.handle_query(request)

  def handle_user(self, request):
    self.handle_query(request)

  def handle_query(self, request):
    d = request.db.runQuery(self.query)
    d.addCallback(self.report_success, request)
    d.addErrback(self.report_error, request)

  def report_success(self, result, request):
    key = request.results.append(result)
    if result:
      request.respond('OK: rows=%d results at %s' %
          (len(result), web.get_url(key)))

  def report_error(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())
