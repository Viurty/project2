

class Logic():

    def __init__(self,data,start,end):
        self.data = data
        self.start = start
        self.end = end

    def check_temperature(self,place):
        if self.data[place]["min_temperature"] > 10 and self.data[place]["max_temperature"] < 30:
            return True
        else:
            return False

    def check_humidity(self,place):
        if 30 < self.data[place]['humidity'] < 70:
            return True
        else:
            return False

    def check_wind(self,place):
        if self.data[place]['wind_speed'] < 25:
            return True
        if self.data[place]['wind_speed'] >50:
            return f'Небезопасно, в городе штормовый ветер'
        return False

    def check_probability(self,place):
        if max(self.data[place]['probability_snow'],self.data[place]['probability_rain']) < 50:
            return True
        else:
            return False

    def get_res_start(self):
        temp = self.check_temperature(self.start)
        humi = self.check_humidity(self.start)
        wind = self.check_wind(self.start)
        if not str(wind) in ['True',"False"]:
            return wind
        prob = self.check_probability(self.start)
        if not temp or not prob:
            return 'red', 'Неблагоприятная погода'
        elif not humi or not wind:
            return 'yellow', 'Удоволетворительная погода'
        else:
            return 'green', 'Отличная погода'

    def get_res_end(self):
        temp = self.check_temperature(self.end)
        humi = self.check_humidity(self.end)
        wind = self.check_wind(self.end)
        if not str(wind) in ['True',"False"]:
            return wind
        prob = self.check_probability(self.end)
        if not temp or not prob:
            return 'red','Не рекомендуем поездку в связи с плохой погодой!'
        elif not humi or not wind:
            return 'yellow', 'Рекомендуем обдумать поездку.'
        else:
            return 'green', 'Оптимальная погода для поездки!'

def days(day):
    if day == 1:
        return '1 день'
    elif day in [2,3,4]:
        return f'{day} дня'
    else:
        return '5 дней'




