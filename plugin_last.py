import cmdbase
import command

class LastCommand(cmdbase.DatabaseCommand):

  def do_last(self, request):
    if request.account in self.users:
      d = self.db.runQuery('SELECT updated, channel, user, message '
                      'FROM lasts WHERE user LIKE ?',
          (request.args[1] + '!%', ))
      d.addCallback(self.reportLast, request)
      d.addErrback(self.reportError, request)
    else:
      d = self.db.runQuery('SELECT updated, channel, user, message '
                      'FROM lasts WHERE user LIKE ? AND channel = ?',
          (request.args[1] + '!%', request.channel))
      d.addCallback(self.reportLast, request)

  def reportLast(self, result, request):
    request.respond('%s %s %s "%s"' % result[0])

def register():
  pass
  #command.CommandHandler.register('boss', BossCommand())
