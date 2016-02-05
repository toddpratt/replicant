import plugin_base
import command

class PingCommand(plugin_base.BaseCommand):

  def handle_admin(self, request):
    request.respond('I am your servant.')

  def handle_user(self, request):
    request.respond('pong.')

def register():
  command.CommandHandler.register('ping', PingCommand())
