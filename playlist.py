import collections
import json
import threading

class Playlist(object):

  def __init__(self, filename):
    self._filename = filename
    self._pl = []
    self._cbs = []

  def append(self, item):
    self._pl.append(item)
    self.save()
    self.do_callbacks()

  def do_callbacks(self):
    for cb in self._cbs:
      cb()

  def clear(self):
    del self._pl[:]

  def get(self):
    return json.dumps(self._pl, separators=(',', ':'))

  def read(self, f):
    self._pl = json.load(f)
    self.do_callbacks()

  def write(self, f):
    json.dump(self._pl, f, indent=2, sort_keys=True)

  def save(self):
    with open(self._filename, "w") as f:
      self.write(f)

  def load(self):
    with open(self._filename) as f:
      self.read(f)

  def addCallback(self, cb):
    self._cbs.append(cb)

  def has_video(self, vid):
    return vid in (e['vid'] for e in self._pl)
