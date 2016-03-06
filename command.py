import pluginreg

class CommandHandler(object):
  commands = {}
  @classmethod
  def register(cls, command, handler):
    cls.commands[command] = handler

  def __init__(self, db, conf, results, catalog):
    self.db = db
    self.conf = conf
    self.results = results
    self._catalog = catalog

  def handle(self, request):
    print request
    try:
      command_name = request.args[0][1:]
      function_name = 'do_' + command_name
    except ValueError:
      pass
    else:
      request.db = self.db
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
    config = self.conf["servers"][request.chatnet]
    if request.account in config["admin-users"]:
      reload(pluginreg)
      pluginreg.reload_commands(self._catalog)
      request.respond('reloaded')
    else:
      request.respond('You ain\'t no admin I ever heard of.')
