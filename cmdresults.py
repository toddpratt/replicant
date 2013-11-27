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
    for index in request.args[1:]:
      try:
        index = int(index)
        request.respond('result set %d has %d entries' %
            (index, len(request.results[index])))
      except (IndexError, ValueError):
        invalids.append(index)
    if invalids:
      request.respond('invalid indices: ' + ', '.join(invalids))

class RSelCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    result_state.results = request.results
    args = request.args
    if len(args) != 2:
      request.respond('usage: rsel <index>')
    else:
      try:
        index = int(request.args[1])
        result_state.select(index)
      except (IndexError, ValueError):
        request.respond('invalid index: %s' % index)

class WriteHistoryCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    reload(config)
    config.save_history(request.lines)

def register_commands():
  command.CommandHandler.register('rc', RCountCommand())
  command.CommandHandler.register('wh', WriteHistoryCommand())
