import glob

import command

def reload_commands():
  names = glob.glob('cmd*.py')
  for name in names:
    module = __import__(name.split('.')[0])
    reload(module)
    registrar = getattr(module, 'register_commands', None)
    if registrar:
      registrar()
