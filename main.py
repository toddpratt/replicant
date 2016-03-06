from twisted.enterprise import adbapi 
from twisted.internet import reactor

import os

import catalog
import command
import pluginreg
import config
import factory
import linerecv
import playlist
import proto
import request
import userdb
import web
import results

if __name__ == '__main__':
  conf = config.Configuration('bot.conf')
  conf.load()
  databases = {}
  servers = {}
  catalog = catalog.Catalog(conf)
  catalog.add('yt_playlist', playlist.Playlist())
  result_sets = results.Results()

  for db_name, db_config in conf['databases'].iteritems():
    databases[db_name] = adbapi.ConnectionPool(*db_config)

  db = databases['default']
  users = userdb.UserDB(db)
  pluginreg.reload_commands(catalog)
  command_handler = command.CommandHandler(
          db, users, conf, result_sets, catalog)

  for server, server_config in conf['servers'].iteritems():
    servers[server] = f = factory.BotFactory()
    f.db = db

    f.ircnet = server
    f.channels = [c for c in server_config['channels']]
    f.irc_host = server_config['host']
    f.irc_port = server_config['port']
    f.nickname = server_config['nickname']
    f.realname = server_config['realname']
    f.password = server_config['password']
    f.username = server_config['username']
    f.prefix = server_config['command_prefix']

    f.conf = conf
    f.users = users
    f.request_factory = request.Request
    f.protocol = proto.BotProtocol
    f.handler = command_handler
    reactor.connectTCP(f.irc_host, f.irc_port, f)

  web.start(result_sets, catalog)
  linerecv.start(command_handler, servers)
  reactor.run()
