from twisted.enterprise import adbapi 
from twisted.internet import reactor

import os

import config
import factory
import proto
import request
import userdb

if __name__ == '__main__':
  conf = config.Configuration('bot.conf')
  databases = {}
  servers = {}
  lines = []

  for db_name, db_config in conf['databases']:
    databases[db_name] = adbapi.ConnectionPool(*db_config)

  for server, server_config in conf['servers'].iteritems():
    servers[server] = f = factory.BotFactory()
    f.db = databases[server_config['database']]

    f.channels = server_config['channels']
    f.irc_host = server_config['host']
    f.irc_port = server_config['port']
    f.nickname = server_config['nickname']
    f.realname = server_config['realname']
    f.password = server_config['password']
    f.username = server_config['username']
    f.prefix = server_config['command_prefix']

    f.conf = conf
    f.lines = lines
    f.users = userdb.UserDB(f.db)
    f.request_factory = request.Request
    f.protocol = proto.BotProtocol
    f.handler = command.CommandHandler(f.db, f.users, lines)
    reactor.connectTCP(f.irc_host, f.irc_port, f, conf)

  reactor.run()
