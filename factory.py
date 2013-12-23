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

  def reconnect(self, connector):
    print 'reconnecting:', connector
    connector.connect()

  def clientConnectionFailed(self, connector, failure):
    self.clientConnectionLost(connector, failure)

  def clientConnectionLost(self, connector, failure):
    print failure.getErrorMessage()
    reactor.callLater(300, self.reconnect, connector)
