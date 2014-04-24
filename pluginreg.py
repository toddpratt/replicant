import glob

import command

def reload_commands():
  names = glob.glob('plugin_*.py')
  for name in names:
    print 'loading module', name
    module = __import__(name.split('.')[0])
    reload(module)
    registrar = getattr(module, 'register', None)
    if registrar:
      registrar()
