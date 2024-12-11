import requests
#'spfT2R28NnnmtGlikbyhDGsr2MR8VJyk'
#CskMp9tC6VxIjbWt72u2J2wxkJyjGgJw
#'Yi2HypX2aKkLobtuwcA96VmxLuDerEZI'
class error503(Exception):
    def __init__(self,text):
        self.txt = text



class Forecast():

    def __init__(self,starting_city,ending_city,day_start,day_end):
        self.api = 'spfT2R28NnnmtGlikbyhDGsr2MR8VJyk'
        self.url_weather = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'
        self.url_city = 'http://dataservice.accuweather.com/locations/v1/cities/search'
        self.start = starting_city
        self.end = ending_city
        self.day_start = day_start - 1
        self.day_end = day_end - 1
        self.data = dict()

    def search_city_start(self):
        r = requests.get(self.url_city,params={'apikey' : self.api, 'q' : self.start})
        if r.status_code == 503:
            raise error503('Проблема с подключением к серверу')
        starting_id = r.json()[0]['Key']
        return starting_id

    def search_city_end(self):
        ending_id = requests.get(self.url_city, params={'apikey': self.api, 'q': self.end}).json()[0]['Key']
        return ending_id

    def get_forecast_start(self):
        city_key = self.search_city_start()
        request_start = requests.get(self.url_weather+city_key,params={'apikey' : self.api, 'details' : True})
        return request_start.json()

    def get_forecast_end(self):
        city_key = self.search_city_end()
        request_end = requests.get(self.url_weather+city_key,params={'apikey' : self.api, 'details' : True})
        return request_end.json()

    def get_data_start(self):
        info_start = self.get_forecast_start()['DailyForecasts'][self.day_start]
        min_temp_start = round((info_start['Temperature']['Minimum']['Value'] - 32)*(5/9),1)
        max_temp_start = round((info_start['Temperature']['Maximum']['Value'] - 32)*(5/9),1)
        hum_start = info_start['Day']['RelativeHumidity']['Average']
        wind_start = round(info_start['Day']['Wind']['Speed']['Value']*1.6,0)
        rain_prob_start = info_start['Day']['RainProbability']
        snow_prob_start = info_start['Day']['SnowProbability']
        self.data[self.start] = {'min_temperature' : min_temp_start, 'max_temperature' : max_temp_start, 'humidity' : hum_start, 'wind_speed' : wind_start,'probability_rain' : rain_prob_start, 'probability_snow' : snow_prob_start}
        data = self.data
        return data

    def get_data_end(self):
        info_end = self.get_forecast_end()['DailyForecasts'][self.day_end]
        min_temp_end = round((info_end['Temperature']['Minimum']['Value'] - 32)*(5/9),1)
        max_temp_end = round((info_end['Temperature']['Maximum']['Value'] - 32)*(5/9),1)
        hum_end = info_end['Day']['RelativeHumidity']['Average']
        wind_end = round(info_end['Day']['Wind']['Speed']['Value']*1.6,0)
        rain_prob_end = info_end['Day']['RainProbability']
        snow_prob_end = info_end['Day']['SnowProbability']
        self.data[self.end] = {'min_temperature' : min_temp_end, 'max_temperature' : max_temp_end, 'humidity' : hum_end, 'wind_speed' : wind_end,'probability_rain' : rain_prob_end, 'probability_snow' : snow_prob_end}
        data = self.data
        return data

    def get_all_data(self):
        self.get_data_start()
        self.get_data_end()
        data = self.data
        return data

    def get_scpecific(self,place):
        data = self.data[place]
        min_temp = str(data['min_temperature'])
        max_temp = str(data['max_temperature'])
        humi = str(data['humidity'])
        prob_rain = data['probability_rain']
        prob_snow = data['probability_snow']
        if prob_snow == 0 and prob_rain == 0:
            prob = 'Осадки не предвидятся'
        elif prob_rain > prob_snow:
            prob = f'Вероятность начала дождя: {prob_rain}%'
        else:
            prob = f'Вероятность выпадения снега: {prob_snow}%'
        wind = data['wind_speed']
        message = f'Минимальная температура: {min_temp}°C\n Максимальная температура: {max_temp}°C\n {prob}\n Влажность воздуха: {humi}%\n Скорость ветра: {wind} км/ч'
        return message
