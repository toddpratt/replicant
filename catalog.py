
class Catalog(object):

  def __init__(self, config):
    self.config = config
    self._catalog = {}

  def get_plugin_config(self, plugin):
    return self.config["plugins"][plugin]

  def add(self, key, value):
    self._catalog[key] = value

  def get(self, key):
    return self._catalog[key]

  def get_channel_config(self, chatnet, channel):
    return self.config['servers'][chatnet]["channels"][channel]

  def save_config(self):
    self.config.save()
