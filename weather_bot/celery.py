import os

from celery import Celery

import django
import os

import telegram
import requests

api_key = '6083081731:AAGTHb_vcXZ0ZHE1_t8bAT9kxI6mIJkZFUw'
WEATHER_API_KEY = 'a9d64e585f21ad027a586d4b39ac7145'
bot = telegram.Bot(token=api_key)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_bot.settings')

django.setup()
from app.models import Subscribers

app = Celery('weather_bot')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def send_update(self):
    for subscriber in Subscribers.objects.all():
        print (subscriber.username)
        weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={subscriber.city}&units=metric&APPID={WEATHER_API_KEY}")
        update = f"City : {weather_data.json()['name']} \nWeather : {weather_data.json()['weather'][0]['main']} \n\nTemperature : {weather_data.json()['main']['temp']} \nFeels Like : {weather_data.json()['main']['feels_like']} \nMinimum Temperature : {weather_data.json()['main']['temp_min']} \nMaximum Temperature : {weather_data.json()['main']['temp_max']} \n\nPressure : {weather_data.json()['main']['pressure']} \nHumidity : {weather_data.json()['main']['humidity']} \nWind Speed : {weather_data.json()['wind']['speed']}"
        print (update)
        bot.send_message(chat_id=subscriber.chat_id, text=update)
        print("Update sent successfully")

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')