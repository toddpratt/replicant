import json

import command
import config
import plugin_base

class SaveCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    self._catalog.config.save()
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
  command.CommandHandler.register('csave', SaveCommand(catalog))
  command.CommandHandler.register('ch', ChangeCommand(catalog))
  command.CommandHandler.register('sh', ShowCommand(catalog))
