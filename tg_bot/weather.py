from datetime import datetime

import requests

from tg_bot import config


class Weather:
    def __init__(self):
        self.code_to_smile = {
            'Clear': 'Ясно \U00002600',
            'Clouds': 'Облачно \U00002601',
            'Rain': 'Дождь \U00002614',
            'Drizzle': 'Дождь \U00002614',
            'Thunderstorm': 'Гроза \U000026A1',
            'Snow': 'Снег \U0001F328',
            'Mist': 'Туман \U0001F32B'
        }

    def get_weather(self, text):
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={text}'
            f'&appid={config.WEATHER_TOKEN}&units=metric'
        )
        data = r.json()

        city = data['name']
        current_weather = data['main']['temp']

        weather_description = data['weather'][0]['main']
        if weather_description in self.code_to_smile:
            wd = self.code_to_smile[weather_description]
        else:
            wd = ''

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
        sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
        length_of_the_day = sunset_timestamp - sunrise_timestamp

        return (
            f'Сегодня: {datetime.now().strftime("%d-%m-%Y %H:%M")}\n'
            f'Погода в городе: {city}\nТемпература: {current_weather}°C {wd}\n'
            f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n'
            f'Ветер: {wind}м/с\nВосход солнца: {sunrise_timestamp}\n'
            f'Закат солнца: {sunset_timestamp}\n'
            f'Продолжительность дня: {length_of_the_day}\n'
        )
    

    def get_week_weather(self, text):
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={text}'
            f'&appid={config.WEATHER_TOKEN}&units=metric&cnt=7'
        )
        data = r.json()

        city = data['name']
        current_weather = data['main']['temp']

        week = []

        for i in range(7):
            weather_description = data['weather'][i]['main']
            if weather_description in self.code_to_smile:
                wd = self.code_to_smile[weather_description]
            else:
                wd = ''

            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind = data['wind']['speed']
            sunrise_timestamp = datetime.fromtimestamp(data['sys']['sunrise'])
            sunset_timestamp = datetime.fromtimestamp(data['sys']['sunset'])
            length_of_the_day = sunset_timestamp - sunrise_timestamp

            day_weather = (
                f'Сегодня: {datetime.now().strftime("%d-%m-%Y %H:%M")}\n',
                f'Погода в городе: {city}\nТемпература: {current_weather}°C {wd}\n',
                f'Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст.\n',
                f'Ветер: {wind}м/с\nВосход солнца: {sunrise_timestamp}\n,'
                f'Закат солнца: {sunset_timestamp}\n',
                f'Продолжительность дня: {length_of_the_day}\n',
                f'\n',
            )
            week.append(day_weather)

        return week
            
