from twisted.internet import protocol
from twisted.internet import reactor

class BotFactory(protocol.ClientFactory):

  reconnect = None

  def buildProtocol(self, addr):
    self.ircbot = proto = self.protocol()
    proto.factory = self
    proto.nickname = self.nickname
    proto.realname = self.realname
    proto.password = self.password
    proto.username = self.nickname
    proto.last_result = tuple()
    proto.iter_result = iter(tuple())
    return self.ircbot

  def clientConnectionLost(self, connector, failure):
    print failure.getErrorMessage()
    if self.reconnect is None:
      self.reconnect = 0
    elif self.reconnect < 20:
      self.reconnect += 5
    reactor.callLater(self.reconnect, connector.connect)
