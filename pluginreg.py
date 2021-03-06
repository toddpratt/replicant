import glob

import command
import proto

def reload_commands(catalog):
  proto.BotProtocol.reset_plugins()
  names = glob.glob('plugin_*.py')
  for name in names:
    print 'loading module', name
    module = __import__(name.split('.')[0])
    reload(module)
    registrar = getattr(module, 'register', None)
    if registrar:
      registrar(catalog)
