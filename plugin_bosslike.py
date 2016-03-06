import plugin_base
import command

class BossCommand(plugin_base.DatabaseCommand):

  def __init__(self, catalog):
    # bypass the DatabaseCommand __init__
    plugin_base.BaseCommand.__init__(self, catalog)

  def runQuery(self, request, query, report_success=None, args=tuple()):
    if report_success is None:
      report_success = self.report_success
    d = self.get_db().runQuery(query, args)
    d.addCallback(report_success, request)
    d.addErrback(self.report_error, request)

  def report_random(self, result, request):
    phrase = result[0][0]
    if 'like a boss' not in phrase:
      phrase = phrase + '... like a boss!!!'
    request.proto.say(request.channel, phrase)

  def handle(self, request):
    args = request.message.split(None, 1)
    print args
    if len(args) == 1:
      query = 'SELECT phrase FROM bosslike ORDER BY RANDOM() LIMIT 1'
      self.runQuery(request, query, report_success=self.report_random)
    elif len(args) == 2:
      query = 'INSERT INTO bosslike (phrase) VALUES (?)'
      self.runQuery(request, query, args=(args[1], ))

def register(catalog):
  command.CommandHandler.register('boss', BossCommand(catalog))
