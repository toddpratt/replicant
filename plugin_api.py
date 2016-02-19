import command
import json
import plugin_base

from twisted.web import client


class JsonApiCommand(plugin_base.BaseCommand):

  def compute_url(self, request):
    config = request.conf['plugins']['weather']
    return (config["url"] + "?zip=" + request.args[1] +
            "&appid=" + config["key"] + "&units=imperial")

  def handle_user(self, request):
    d = client.getPage(self.compute_url(request).encode('utf-8'))
    d.addCallback(self._report_success, request)
    d.addErrback(self.report_failure, request)

  def _report_success(self, results, request):
    self.report_success(json.loads(results), request)

  def report_success(self, results, request):
    city = results["name"]
    description = results["weather"][0]["description"]
    temp = results["main"]["temp"]
    humidity = results["main"]["humidity"]
    request.respond("City: %(city)s: Temp: %(temp)sF "
                    "Humidity: %(humidity)s%% "
                    "conditions: %(description)s" % {
                        "city": city, "description": description,
                        "temp": temp, "humidity": humidity})

  def report_failure(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())


def register():
  command.CommandHandler.register('w', WeatherCommand())
