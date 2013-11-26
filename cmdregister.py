import command

import cmdbase
import cmdgrep
import cmdping
import cmdquery

modules = [
    cmdbase,
    cmdgrep,
    cmdping,
    cmdquery
]

def register_commands():
  for module in modules:
    module.register_commands()

def reload_commands():
  for module in modules:
    reload(module)
  register_commands()
