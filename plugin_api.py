import command
import json
import plugin_base

from twisted.web import client


class JsonApiCommand(plugin_base.BaseCommand):

  def compute_url(self, request):
    return "url"

  def report_success(self, results, request):
    request.respond("it worked.")

  def handle_user(self, request):
    d = client.getPage(self.compute_url(request).encode('utf-8'))
    d.addCallback(self._report_success, request)
    d.addErrback(self.report_failure, request)

  def _report_success(self, results, request):
    self.report_success(json.loads(results), request)

  def report_failure(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())
