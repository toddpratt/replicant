import json

import cmdbase
import command

class SaveCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    request.conf.save()
    request.respond('OK')

class ChangeCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    _, key, data = request.message.split(None, 2)
    parts = key.split('.')
    target = request.conf
    for part in parts[:-1]:
      target = target[part]
    target[parts[-1]] = json.loads(data) 
    request.respond(key + ': OK')

def register():
  command.CommandHandler.register('csave', SaveCommand())
  command.CommandHandler.register('ch', ChangeCommand())
