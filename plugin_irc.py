import plugin_base
import command

class IrcCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    method_name = request.args[1]
    args = request.args[2:]
    method = getattr(request.proto, method_name, None)
    if method:
      method(*args)
      request.respond('Okay')
    else:
      request.respond('%s: no method' % method_name)

class OpCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    request.proto.mode(request.channel, True, 'o', user=request.args[1])

class OpmeCommand(plugin_base.BaseAdminCommand):

  def handle_user(self, request):
    query = 'SELECT COUNT(*) FROM ops WHERE channel = ? AND account = ?'

    def success(results, request):
      if results[0][0] == 1:
        request.proto.mode(request.channel, True, 'o', user=request.nick)
      else:
        request.respond('you ain\'t no op I ever heard of')

    def failure(failure, request):
      request.respond('error: %s' % failure.getErrorMessage())

    d = request.db.runQuery(query, (request.channel, request.account))
    d.addCallback(success, request)
    d.addErrback(failure, request)

  def handle_admin(self, request):
    self.handle_user(request)

class OpsCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    query = 'SELECT account FROM ops WHERE channel = ?'

    def success(results, request):
      if results:
        request.respond('ops: ' + ', '.join(e[0] for e in results))
      else:
        request.respond('I don\'t know of any ops on this channel.')

    d = request.db.runQuery(query, (request.channel, ))
    d.addCallback(success, request)

def register():
  command.CommandHandler.register('irc', IrcCommand())
  command.CommandHandler.register('op', OpCommand())
  command.CommandHandler.register('ops', OpsCommand())
  command.CommandHandler.register('opme', OpmeCommand())
