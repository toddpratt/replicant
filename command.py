import pluginreg

class CommandHandler(object):
  commands = {}
  @classmethod
  def register(cls, command, handler):
    cls.commands[command] = handler

  def __init__(self, db, users, lines, conf, results):
    self.db = db
    self.users = users
    self.lines = lines
    self.conf = conf
    self.results = results

  def handle(self, request):
    print request
    try:
      command_name = request.args[0][1:]
      function_name = 'do_' + command_name
    except ValueError:
      pass
    else:
      request.db = self.db
      request.users = self.users
      request.lines = self.lines
      request.conf = self.conf
      request.results = self.results
      if command_name in self.commands:
        self.commands[command_name].handle(request)
      else:
        getattr(self, function_name, lambda _: None)(request)

  def do_help(self, request):
    request.respond('base commands: help, say, reload')
    request.respond('registered commands: ' + ', '.join(self.commands))

  def do_reload(self, request):
    if request.account in self.users:
      reload(pluginreg)
      pluginreg.reload_commands()
      request.respond('reloaded')
    else:
      request.respond('You ain\'t no admin I ever heard of.')
