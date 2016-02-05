import plugin_base
import command

class QueryCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    query = request.message.split(None, 1)[1]
    command = plugin_base.DatabaseCommand(query)
    command.handle_user(request)

def register():
  command.CommandHandler.register('query', QueryCommand())
