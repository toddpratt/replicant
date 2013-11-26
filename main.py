from twisted.enterprise import adbapi 
from twisted.internet import reactor

import factory
import proto
import request
import userdb

if __name__ == '__main__':
  f = factory.BotFactory()
  f.db = adbapi.ConnectionPool('sqlite3', 'db.sqlite3')
  f.users = userdb.UserDB(f.db)
  f.protocol = proto.BotProtocol
  f.channels = { '#nerdism' }
  f.lines = []
  f.irc_host = 'Chicago.IL.US.Undernet.Org'
  f.irc_port = 6669
  f.nickname = "replicant"
  f.realname = "Roy Batty"
  f.password = None
  f.username = f.nickname
  f.request_factory = request.Request
  f.master = 'sucralose'
  f.prefix = '@'

  reactor.connectTCP(f.irc_host, f.irc_port, f)
  reactor.run()
