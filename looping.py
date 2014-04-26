from twisted.internet import task

_loopers = {}

def register(name, fn, interval, now, *args, **kwargs):
  lc = _loopers.get(name)
  if lc and lc.running:
    lc.stop()
  lc = task.LoopingCall(fn, *args, **kwargs)
  _loopers[name] = lc
  lc.start(interval, now=now)

def stop(name):
  lc = _loopers.get(name)
  if lc and lc.running:
    lc.stop()
    del _loopers[name]

def is_running(name):
  lc = _loopers.get(name)
  return lc is not None and lc.running

