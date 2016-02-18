import command
import json
import plugin_base

from twisted.web import client


class WeatherCommand(plugin_base.BaseCommand):

  def handle_user(self, request):
    config = request.conf['plugins']['weather']
    url = (
        config["url"].encode("utf-8") +
        "?zip=" + request.args[1] +
        "&appid=" + config["key"].encode("utf-8") +
        "&units=imperial")
    d = client.getPage(url)
    d.addCallback(self.report_weather, request)
    d.addErrback(self.report_problem, request)

  def report_weather(self, results, request):
    results = json.loads(results)
    city = results["name"].encode("utf-8")
    description = results["weather"][0]["description"].encode("utf-8")
    temp = results["main"]["temp"]
    humidity = results["main"]["humidity"]
    request.respond("City: %(city)s: Temp: %(temp)sF "
                    "Humidity: %(humidity)s%% "
                    "conditions: %(description)s" % {
                        "city": city, "description": description,
                        "temp": temp, "humidity": humidity})

  def report_problem(self, failure, request):
    request.respond('error: %s' % failure.getErrorMessage())


def register():
  command.CommandHandler.register('w', WeatherCommand())
