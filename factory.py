from twisted.internet import protocol
from twisted.internet import reactor

class BotFactory(protocol.ClientFactory):

  def buildProtocol(self, addr):
    self.ircbot = proto = self.protocol()
    proto.factory = self
    proto.nickname = self.nickname
    proto.realname = self.realname
    proto.password = self.password
    proto.username = self.nickname
    return self.ircbot

  def clientConnectionLost(self, connector, failure):
    print failure.getErrorMessage()
    reactor.callLater(10, connector.connect)
