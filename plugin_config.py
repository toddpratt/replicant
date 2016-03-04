import json

import command
import config
import plugin_base

class SaveCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    request.conf.save()
    request.respond('OK')

class ChangeCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    _, key, data = request.message.split(None, 2)
    key, target = request.conf.get_parent(key)
    target[key] = json.loads(data) 
    request.respond(key + ': OK')

class ShowCommand(plugin_base.BaseAdminCommand):
  
  def handle_admin(self, request):
    _, key = request.message.split(None, 2)
    key, target = request.conf.get_parent(key)
    request.respond(json.dumps(target[key]))

def register(catalog):
  reload(config)
  command.CommandHandler.register('csave', SaveCommand())
  command.CommandHandler.register('ch', ChangeCommand())
  command.CommandHandler.register('sh', ShowCommand())
