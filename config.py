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

  def __getitem__(self, name):
    return self._config[name]
