import cmdbase
import command

class IrcCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    method_name = request.args[1]
    args = request.args[2:]
    method = getattr(request.proto, method_name, None)
    if method:
      method(*args)
      request.respond('Okay')
    else:
      request.respond('%s: no method' % method_name)

class OpCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    request.proto.mode(request.channel, True, 'o', user=request.args[1])

class OpmeCommand(cmdbase.BaseAdminCommand):

  def handle_user(self, request):
    query = 'SELECT COUNT(*) FROM ops WHERE channel = ? AND account = ?'

    def success(results, request):
      if results[0][0] == 1:
        request.proto.mode(request.channel, True, 'o', user=request.nick)
      else:
        request.respond('you aint no op I ever heard of')

    def failure(failure, request):
      request.respond('error: %s' % failure.getErrorMessage())

    d = request.db.runQuery(query, (request.channel, request.account))
    d.addCallback(success, request)
    d.addErrback(failure, request)

  def handle_admin(self, request):
    self.handle_user(request)

def register_commands():
  command.CommandHandler.register('irc', IrcCommand())
  command.CommandHandler.register('op', OpCommand())
  command.CommandHandler.register('opme', OpmeCommand())
