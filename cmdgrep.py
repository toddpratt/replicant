import re

import cmdbase
import command

class GrepCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    regexes = [re.compile(p) for p in request.args[1:]]
    result = []
    for line in request.lines:
      if any(p.search(line) for p in regexes):
        result.append(line)
    request.results.append(result)
    request.respond('%d matches' % len(result))

def register_commands():
  command.CommandHandler.register('grep', GrepCommand())
