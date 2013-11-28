import cmdbase
import command

class IrcCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    method_name = request.args[1]
    args = request.args[2:]
    method = getattr(request.proto, method_name, lambda *args: None)(*args)
    request.respond('Okay')

def register_commands():
  command.CommandHandler.register('irc', IrcCommand())
