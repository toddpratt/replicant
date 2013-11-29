import cmdbase
import command

class BaseBosslikeCommand(cmdbase.DatabaseCommand):

  def __init__(self):
    pass

  def runQuery(self, request, query, *args):
    d = request.db.runQuery(query, *args)
    d.addCallback(self.report_success, request)
    d.addErrback(self.report_error, request)

class AddBosslikeCommand(BaseBosslikeCommand):

  def handle(self, request):
    phrase = request.message.split(None, 1)[1]
    query = 'INSERT INTO bosslike (phrase) VALUES (?)'
    self.runQuery(request, query, (phrase, ))

class BossRandomCommand(BaseBosslikeCommand):
 
  def handle(self, request):
    query = 'SELECT phrase FROM bosslike ORDER BY RANDOM() LIMIT 1'
    self.runQuery(request, query)

  def report_success(self, result, request):
    request.respond(result[0][0].encode('utf-8') + '... like a boss!!!')


def register_commands():
  command.CommandHandler.register(
      'bosslike', cmdbase.DatabaseCommand('SELECT phrase FROM bosslike'))

  command.CommandHandler.register('addbosslike', AddBosslikeCommand())

  boss_command = BossRandomCommand()
  command.CommandHandler.register('bossrandom', boss_command)
  command.CommandHandler.register('boss', boss_command)
