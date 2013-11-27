import random
import string

def get_candidate_key():
  return ''.join(random.sample(string.letters, 8))

class Results(object):

  def __init__(self):
    self._results = {}

  def append(self, data):
    key = get_candidate_key()
    while self._results.setdefault(key, data) is not data:
      key = get_candidate_key()
    return key

  def iterkeys(self):
    return self._results.iterkeys()

  def __getitem__(self, key):
    return self._results[key]
