import cmdbase
import command
import config

class ResultState(object):

  def __init__(self):
    self.results = None
    self.selected = None

  def select(self, index):
    self.selected = iter(self.results[index])

result_state = ResultState()

class RCountCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    request.respond('result set count: %d' % len(request.results))
    invalids = []
    for key in request.args[1:]:
      try:
        request.respond('result set %d has %d entries' %
            (key, len(request.results[key])))
      except KeyError:
        invalids.append(key)
    if invalids:
      request.respond('invalid keys: ' + ', '.join(invalids))

class WriteHistoryCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    reload(config)
    config.save_history(request.lines)

def register_commands():
  command.CommandHandler.register('rc', RCountCommand())
  command.CommandHandler.register('wh', WriteHistoryCommand())
