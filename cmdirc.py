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

def register_commands():
  command.CommandHandler.register('irc', IrcCommand())
