import plugin_base
import command

import json
import urlparse
import urllib2

class PlaylistError(Exception):
  pass


class PlaylistClearCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    request.proto.factory.youtube_playlist.clear()
    request.respond("OK")


class PlaylistCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    self.handle_user(request)

  def handle_user(self, request):
    url = request.args[1]
    result = urlparse.urlparse(url)
    conf = request.conf['plugins']['youtube']
    playlist = request.proto.factory.youtube_playlist
    try:
      if result.scheme not in ('http', 'https'):
        raise PlaylistError("Invalid URL scheme.")

      if result.netloc not in conf['netlocs']:
        raise PlaylistError("Invalid hostname.")

      if len(result.path) == 14 and result.path.startswith("/v/"):
        vid = result.path[3:]
      elif len(result.path) == 12:
        vid = result.path[1:]
      elif result.path == "/watch":
        query = urlparse.parse_qs(result.query)
        vid = query['v'][0]
      else:
        raise PlaylistError("Unable to determine video id.")

      if playlist.has_video(vid):
        raise PlaylistError("That video is already listed.")

      info_url = conf['info_url'] % {"key": conf['key'], "vid": vid}
      info = json.load(urllib2.urlopen(info_url))
      playlist.append({"user": request.nick, "vid": vid, "data": info})
      request.respond(info["items"][0]["snippet"]["title"] + ": OK")
    except PlaylistError as err:
      request.respond(err.args[0])


def register():
  command.CommandHandler.register('pl', PlaylistCommand())
  command.CommandHandler.register('plx', PlaylistClearCommand())
