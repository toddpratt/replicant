import re

import cmdbase
import command
import web

class GrepCommand(cmdbase.BaseAdminCommand):

  def handle_admin(self, request):
    regexes = [re.compile(p) for p in request.args[1:]]
    result = []
    for line in request.lines:
      if any(p.search(line) for p in regexes):
        result.append(line)
    key = request.results.append(result)
    request.respond('%d matches see results at: %s' %
        (len(result), web.get_url(key)))

def register_commands():
  command.CommandHandler.register('grep', GrepCommand())
