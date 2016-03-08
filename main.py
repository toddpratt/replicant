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
import web
import results

if __name__ == '__main__':
  conf = config.Configuration('bot.conf')
  conf.load()
  databases = {}
  servers = {}
  ctlg = catalog.Catalog(conf)
  ytpl = playlist.Playlist(ctlg.get_plugin_config('youtube')['filename'])
  ytpl.load()
  ctlg.add('yt_playlist', ytpl)
  ctlg.add('databases', databases)
  ctlg.add('servers', servers)
  result_sets = results.Results()

  for db_name, db_config in conf['databases'].iteritems():
    databases[db_name] = adbapi.ConnectionPool(*db_config)

  db = databases['default']
  pluginreg.reload_commands(ctlg)
  command_handler = command.CommandHandler(
          conf, result_sets, ctlg)

  for server, server_config in conf['servers'].iteritems():
    servers[server] = f = factory.BotFactory()

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
    f.request_factory = request.Request
    f.protocol = proto.BotProtocol
    f.handler = command_handler
    reactor.connectTCP(f.irc_host, f.irc_port, f)

  web.start(result_sets, ctlg)
  linerecv.start(command_handler, servers)
  reactor.run()
