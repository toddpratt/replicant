import plugin_base
import command

import hashlib
import random
import sys

challenges = {}
password = "hard4u2Ges"

class AuthCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    value = challenges.get(request.account)
    if value and len(request.args) == 2 and value == request.args[1]:
      request.users.append(request.account)
      request.respond("ok")
    elif value:
      del challenges[request.account]
      request.respond("challenge aborted.")
    else:
      md5 = hashlib.md5(
              str(random.randint(sys.maxint/2, sys.maxint))).hexdigest()
      challenges[request.account] = hashlib.md5(
              password + md5 + '\n').hexdigest()
      request.respond(md5)

class IrcCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    method_name = request.args[1]
    args = request.args[2:]
    method = getattr(request.proto, method_name, None)
    if method:
      method(*args)
      request.respond('Okay')
    else:
      request.respond('%s: no method' % method_name)

class OpCommand(plugin_base.BaseAdminCommand):

  def handle_user(self, request):
    request.proto.mode(request.channel, True, 'o', user=request.args[1])

class OpmeCommand(plugin_base.BaseAdminCommand):

  def handle_user(self, request):
    query = 'SELECT COUNT(*) FROM ops WHERE channel = ? AND account = ?'

    def success(results, request):
      if results[0][0] == 1:
        request.proto.mode(request.channel, True, 'o', user=request.nick)
      else:
        request.respond('you ain\'t no op I ever heard of')

    def failure(failure, request):
      request.respond('error: %s' % failure.getErrorMessage())

    d = self.get_db().runQuery(query, (request.channel, request.account))
    d.addCallback(success, request)
    d.addErrback(failure, request)

  def handle_admin(self, request):
    self.handle_user(request)

class OpsCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    query = 'SELECT account FROM ops WHERE channel = ?'

    def success(results, request):
      if results:
        request.respond('ops: ' + ', '.join(e[0] for e in results))
      else:
        request.respond('I don\'t know of any ops on this channel.')

    d = self.get_db().runQuery(query, (request.channel, ))
    d.addCallback(success, request)

class InviteCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    request.proto.invite(request.nick, request.args[1])

def register(catalog):
  command.CommandHandler.register('auth', AuthCommand(catalog))
  command.CommandHandler.register('irc', IrcCommand(catalog))
  command.CommandHandler.register('op', OpCommand(catalog))
  command.CommandHandler.register('ops', OpsCommand(catalog))
  command.CommandHandler.register('opme', OpmeCommand(catalog))
