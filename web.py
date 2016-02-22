from twisted.internet import reactor
from twisted.web import resource
from twisted.web import server
from twisted.web import static

class ResultsResource(resource.Resource):

  def __init__(self, results):
    resource.Resource.__init__(self)
    self.results = results

  def getChild(self, path, request):
    lines = self.results[path]
    return TextResource('\n'.join(str(l) for l in lines))

  def render_GET(self, request):
    request.setHeader('content-type', 'text/plain')
    return '%d results available' % len(self.results)

class TextResource(resource.Resource):

  def __init__(self, text):
    self.text = text

  def render_GET(self, request):
    request.setHeader('content-type', 'text/plain')
    return self.text

class PlaylistPushResource(resource.Resource):

  def __init__(self, urls):
    self._requests = []
    urls.addCallback(self.new_data_received)

  def new_data_received(self):
    for request in self._requests:
      request.finish()
    self._requests = []

  def render_GET(self, request):
    request.setHeader('content-type', 'application/json')
    self._requests.append(request)
    return server.NOT_DONE_YET

class PlaylistResource(resource.Resource):

  def __init__(self, urls):
    self.urls = urls

  def render_GET(self, request):
    request.setHeader('content-type', 'application/json')
    return self.urls.get()

def get_url(name):
    return 'http://104.131.128.201:8000/results/%s' % name

def start(results, playlist):
  root = static.File("html")
  root.putChild('results', ResultsResource(results))
  root.putChild('playlist', PlaylistResource(playlist))
  root.putChild('playlist_push', PlaylistPushResource(playlist))
  site = server.Site(root)
  reactor.listenTCP(8000, site)
