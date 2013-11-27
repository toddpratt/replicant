import cmdbase
import command

class QueryCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    query = request.message.split(None, 1)[1]
    command = cmdbase.DatabaseCommand(query)
    command.handle_user(request)

def register_commands():
  command.CommandHandler.register('query', QueryCommand())
