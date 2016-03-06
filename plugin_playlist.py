import command
import json
import plugin_base
import urlparse
import urllib2

from twisted.web import client

class PlaylistError(Exception):
  pass


class PlaylistClearCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    self._catalog.get('yt_playlist').clear()
    request.respond("OK")


class PlaylistSaveCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    filename = "playlists.json" # % request.args[1]
    with open(filename, "wb") as f:
      self._catalog.get('yt_playlist').write(f)
      request.respond("saved")


class PlaylistLoadCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    filename = "playlists.json" # % request.args[1]
    with open(filename) as f:
      self._catalog.get('yt_playlist').read(f)
      request.respond("loaded")


class PlaylistCommand(plugin_base.BaseAdminCommand):

  def handle_admin(self, request):
    self.handle_user(request)

  def handle_user(self, request):
    url = request.args[1]
    result = urlparse.urlparse(url)
    conf = self._catalog.get_plugin_config('youtube')
    playlist = self._catalog.get('yt_playlist')
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
      d = client.getPage(info_url.encode('utf-8'))
      d.addCallback(self.video_info_success, request, vid)
      d.addErrback(self.video_info_failure, request, vid)
    except PlaylistError as err:
      request.respond(err.args[0])

  def video_info_success(self, info, request, vid):
    info = json.loads(info)
    playlist = self._catalog.get('yt_playlist')
    playlist.append({"user": request.nick, "vid": vid, "data": info})
    request.respond(info["items"][0]["snippet"]["title"] + ": OK")

  def video_info_failure(self, failure, request, vid):
    request.respond("Error: " + failure.getErrorMessage())

def register(catalog):
  command.CommandHandler.register('pl', PlaylistCommand())
  command.CommandHandler.register('plx', PlaylistClearCommand())
  command.CommandHandler.register('plsave', PlaylistSaveCommand(catalog))
  command.CommandHandler.register('plload', PlaylistLoadCommand(catalog))
