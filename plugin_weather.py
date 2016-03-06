import command
import plugin_api


class WeatherCommand(plugin_api.JsonApiCommand):

  def compute_url(self, request):
    values = dict(self.config("weather"))
    values['zip'] = request.args[1]
    return "%(url)s?zip=%(zip)s&appid=%(key)s&units=imperial" % values

  def report_success(self, results, request):
    values = {
        'city': results['name'],
        'description': results['weather'][0]['description'],
        'temp': results['main']['temp'],
        'humidity': results['main']['humidity'],
    }
    request.respond("City: %(city)s: Temp: %(temp)sF "
                    "Humidity: %(humidity)s%% "
                    "conditions: %(description)s" % values)


def register(catalog):
  command.CommandHandler.register('w', WeatherCommand(catalog))
