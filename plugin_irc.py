import json

import plugin_base
import command

class IrcCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    method_name = request.args[1]
    args = request.args[2:]
    method = getattr(request.proto, method_name, None)
    if method:
      try:
        args = [json.loads(s) for s in args]
      except ValueError:
        try:
          args = json.loads(request.message)
        except ValueError:
          pass
      method(*args)
      request.respond('Okay')
    else:
      request.respond('%s: no method' % method_name)

class OpCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    request.proto.mode(request.channel, True, 'o', user=request.args[1])

class OpmeCommand(plugin_base.BaseAdminCommand):

  def handle_user(self, request):
    ch_cfg = self._catalog.get_channel_config(request.chatnet, request.channel)
    if request.account in ch_cfg["operators"]:
      request.proto.mode(request.channel, True, 'o', user=request.nick)
    else:
      request.respond('you ain\'t no op I ever heard of')

  def handle_admin(self, request):
    request.proto.mode(request.channel, True, 'o', user=request.nick)

class InviteCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    request.proto.invite(request.nick, request.args[1])

def register(catalog):
  command.CommandHandler.register('auth', AuthCommand(catalog))
  command.CommandHandler.register('irc', IrcCommand(catalog))
  command.CommandHandler.register('op', OpCommand(catalog))
  command.CommandHandler.register('opme', OpmeCommand(catalog))
