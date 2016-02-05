import json
import os

class Configuration(object):

  def __init__(self, filename):
    self.filename = filename
    self._config = None

  def load(self):
    if os.path.isfile(self.filename):
      with open(self.filename) as config_file:
        self._config = json.load(config_file)
    else:
      self._config = {
        'servers': {
          'undernet': {
            'host': 'chicago.il.us.undernet.org',
            'port': 6669,
            'nickname': 'uselessbot',
            'realname': 'Useless Bot',
            'password': None,
            'username': 'uselessbot',
            'command_prefix': '@',
            'channels': ['#nerdism'],
            'database': 'default',
          },
        },
        'databases': {
          'default': ['sqlite3', 'db.sqlite3'],
        },
      }

  def save(self):
    with open(self.filename, 'w') as config_file:
      json.dump(self._config, config_file, indent=2)

  def get_parent(self, path):
    parts = path.split('.')
    target = self
    for part in parts[:-1]:
      target = target[part]
    return parts[-1], target

  def __getitem__(self, name):
    return self._config[name]

def load_history():
  if os.path.isfile('history'):
    with open('history') as f:
      return [l.strip() for l in f]
  else:
    return []

def save_history(lines):
  with open('history', 'w') as f:
    f.writelines(l + '\n' for l in lines)
