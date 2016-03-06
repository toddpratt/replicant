import command
import web

class BaseCommand(object):

  def __init__(self, catalog=None):
    self._catalog = catalog

  def get_admin_users(self, chatnet):
    return self._catalog.config["servers"][chatnet]['admin-users']

  def handle(self, request):
    if request.account in self.get_admin_users(request.chatnet):
      self.handle_admin(request)
    else:
      self.handle_user(request)

  def handle_admin(self, request):
    self.handle_user(request)

  def handle_user(self, request):
    raise NotImplementedError('override handle_admin')

  def config(self, name):
    return self._catalog.get_plugin_config(name)


class BaseAdminCommand(BaseCommand):

  def handle_admin(self, request):
    raise NotImplementedError('override handle_admin')

  def handle_user(self, request):
    request.respond('You need to be an administrator for that command.')

class DatabaseCommand(BaseAdminCommand):

  def __init__(self, query, catalog=None):
    super(DatabaseCommand, self).__init__(catalog=catalog)
    self.query = query

  def get_db(self):
    return self._catalog.get('databases')['default']

  def handle_admin(self, request):
    self.handle_query(request)

  def handle_user(self, request):
    self.handle_query(request)

  def handle_query(self, request, args=tuple()):
    d = self.get_db().runQuery(self.query, args)
    d.addCallback(self.report_success, request)
    d.addErrback(self.report_error, request)

  def report_success(self, result, request):
    key = request.results.append(result)
    if result:
      request.respond('OK: rows=%d results at %s' %
          (len(result), web.get_url(key)))

  def report_error(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())
