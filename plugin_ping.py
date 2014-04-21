import cmdbase
import command

class PingCommand(cmdbase.BaseCommand):

  def handle_admin(self, request):
    request.respond('I am your servent.')

  def handle_user(self, request):
    request.respond('pong.')

def register():
  command.CommandHandler.register('ping', PingCommand())
