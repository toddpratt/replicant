import collections
import json
import threading

class Playlist(object):

  def __init__(self):
    self._pl = collections.deque((), 10)
    self._cbs = []

  def append(self, item):
    self._pl.appendleft(item)
    for cb in self._cbs:
      cb()

  def clear(self):
    del self._pl[:]

  def get(self):
    return json.dumps(tuple(self._pl))

  def addCallback(self, cb):
    self._cbs.append(cb)

  def has_video(self, vid):
    return vid in (e['vid'] for e in self._pl)
