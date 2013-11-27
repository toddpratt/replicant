import command

import cmdconfig
import cmdgrep
import cmdping
import cmdquery
import cmdresults

modules = [
    cmdconfig,
    cmdgrep,
    cmdping,
    cmdquery,
    cmdresults,
]

def register_commands():
  for module in modules:
    module.register_commands()

def reload_commands():
  for module in modules:
    reload(module)
  register_commands()
