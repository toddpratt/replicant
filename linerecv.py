from twisted.internet import reactor
from twisted.internet import protocol
from twisted.protocols import basic

import request

class TcpInterface(basic.LineReceiver):

  def __init__(self):
    self.server = None

  def connectionMade(self, *args):
    print args
    self.sendLine('hello')

  def lineReceived(self, line):
    args = line.split()
    proto = None

    if len(args) == 1 and args[0] == 'servers':
      self.sendLine('servers: ' + ', '.join(self.factory.servers.iterkeys()))
    elif (len(args) == 2 and args[0] == 'server'
          and args[1] in self.factory.servers):
      self.server = args[1]
      self.sendLine('OK: ' + self.server)
      return
    elif not self.server:
      if len(self.factory.servers) == 1:
        self.server = next(self.factory.servers.iterkeys())
      else:
        self.sendLine('no server chosen')
        return

    proto = self.factory.servers[self.server].ircbot
    request = self.factory.request_factory(
        'localuser!~localuser@localuser.localhost',
        'rawtcp', line, self.respond, proto)

    self.factory.handler.handle(request)

  def respond(self, request, message):
    self.sendLine(message)

def start(handler, servers):
  f = protocol.ServerFactory()
  f.protocol = TcpInterface
  f.request_factory = request.Request
  f.handler = handler
  f.servers = servers
  reactor.listenTCP(8021, f)
