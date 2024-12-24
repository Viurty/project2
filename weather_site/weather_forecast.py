import requests
#'spfT2R28NnnmtGlikbyhDGsr2MR8VJyk' !!!
#CskMp9tC6VxIjbWt72u2J2wxkJyjGgJw
#'Yi2HypX2aKkLobtuwcA96VmxLuDerEZI'
class error503(Exception):
    def __init__(self,text):
        self.txt = text



class Forecast():

    def __init__(self,starting_city,ending_city):
        self.api = 'Rg2Bp0Mxu9Lpz4uabYzfOZuEbrt1pKP9'
        self.url_weather = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/'
        self.url_city = 'http://dataservice.accuweather.com/locations/v1/cities/search'
        self.start = starting_city
        self.end = ending_city
        self.data = dict()

    def search_city(self,city):
        r = requests.get(self.url_city,params={'apikey' : self.api, 'q' : city})
        if r.status_code == 503:
            raise error503('Проблема с подключением к серверу')
        lat = r.json()[0]['GeoPosition']['Latitude']
        lon = r.json()[0]['GeoPosition']['Longitude']
        city_id = r.json()[0]['Key']
        return city_id, lat, lon

    def search_city_start(self):
        r = requests.get(self.url_city,params={'apikey' : self.api, 'q' : self.start})
        if r.status_code == 503:
            raise error503('Проблема с подключением к серверу')
        lat = r.json()[0]['GeoPosition']['Latitude']
        lon = r.json()[0]['GeoPosition']['Longitude']
        starting_id = r.json()[0]['Key']
        return starting_id, lat, lon

    def search_city_end(self):
        r = requests.get(self.url_city, params={'apikey': self.api, 'q': self.end})
        if r.status_code == 503:
            raise error503('Проблема с подключением к серверу')
        lat = r.json()[0]['GeoPosition']['Latitude']
        lon = r.json()[0]['GeoPosition']['Longitude']
        ending_id = r.json()[0]['Key']
        return ending_id, lat, lon

    def get_forecast(self,city):
        city_key, lat, lon = self.search_city(city)
        request = requests.get(self.url_weather+city_key,params={'apikey' : self.api, 'details' : True})
        return request.json(), lat, lon

    def get_forecast_start(self):
        city_key, lat, lon = self.search_city_start()
        request_start = requests.get(self.url_weather+city_key,params={'apikey' : self.api, 'details' : True})
        return request_start.json(), lat, lon

    def get_forecast_end(self):
        city_key, lat, lon = self.search_city_end()
        request_end = requests.get(self.url_weather+city_key,params={'apikey' : self.api, 'details' : True})
        return request_end.json(), lat, lon

    def get_data(self,city):
        self.data[city] = {}
        info, lat, lon = self.get_forecast(city)
        info = info['DailyForecasts']
        for cnt in range(5):
            info_day = info[cnt]
            min_temp_start = round((info_day['Temperature']['Minimum']['Value'] - 32)*(5/9),1)
            max_temp_start = round((info_day['Temperature']['Maximum']['Value'] - 32)*(5/9),1)
            hum_start = info_day['Day']['RelativeHumidity']['Average']
            wind_start = round(info_day['Day']['Wind']['Speed']['Value']*1.6,0)
            rain_prob_start = info_day['Day']['RainProbability']
            snow_prob_start = info_day['Day']['SnowProbability']
            prob = max(rain_prob_start,snow_prob_start)
            self.data[city][f"Day {cnt+1}"] = {'day' : cnt+1,'min_temperature' : min_temp_start, 'max_temperature' : max_temp_start, 'humidity' : hum_start, 'wind_speed' : wind_start,'probability_rain' : rain_prob_start, 'probability_snow' : snow_prob_start,'chance_fallout':prob,'lat':lat,'lon':lon}
        data = self.data
        return data

    def get_data_start(self):
        self.data[self.start] = {}
        info, lat, lon = self.get_forecast_start()
        info = info['DailyForecasts']
        for cnt in range(5):
            info_start = info[cnt]
            min_temp_start = round((info_start['Temperature']['Minimum']['Value'] - 32)*(5/9),1)
            max_temp_start = round((info_start['Temperature']['Maximum']['Value'] - 32)*(5/9),1)
            hum_start = info_start['Day']['RelativeHumidity']['Average']
            wind_start = round(info_start['Day']['Wind']['Speed']['Value']*1.6,0)
            rain_prob_start = info_start['Day']['RainProbability']
            snow_prob_start = info_start['Day']['SnowProbability']
            prob = max(rain_prob_start, snow_prob_start)
            self.data[self.start][f"Day {cnt+1}"] = {'day' : cnt+1,'min_temperature' : min_temp_start, 'max_temperature' : max_temp_start, 'humidity' : hum_start, 'wind_speed' : wind_start,'probability_rain' : rain_prob_start, 'probability_snow' : snow_prob_start,'chance_fallout':prob,'lat':lat,'lon':lon}
        data = self.data
        return data

    def get_data_end(self):
        self.data[self.end] = {}
        info, lat, lon = self.get_forecast_end()
        info = info['DailyForecasts']
        for cnt in range(5):
            info_end = info[cnt]
            min_temp_end = round((info_end['Temperature']['Minimum']['Value'] - 32)*(5/9),1)
            max_temp_end = round((info_end['Temperature']['Maximum']['Value'] - 32)*(5/9),1)
            hum_end = info_end['Day']['RelativeHumidity']['Average']
            wind_end = round(info_end['Day']['Wind']['Speed']['Value']*1.6,0)
            rain_prob_end = info_end['Day']['RainProbability']
            snow_prob_end = info_end['Day']['SnowProbability']
            prob = max(rain_prob_end, snow_prob_end)
            self.data[self.end][f"Day {cnt+1}"] = {'day' : cnt+1,'min_temperature' : min_temp_end, 'max_temperature' : max_temp_end, 'humidity' : hum_end, 'wind_speed' : wind_end,'probability_rain' : rain_prob_end, 'probability_snow' : snow_prob_end,'chance_fallout':prob,'lat':lat,'lon':lon}
        data = self.data
        return data

    def get_all_data(self):
        data = self.data
        return data

    def get_scpecific(self,place,day):
        data = self.data[place][f"Day {day}"]
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
