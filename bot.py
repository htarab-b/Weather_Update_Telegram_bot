from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import Filters

import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'weather_bot.settings'
django.setup()
from app.models import Subscribers
import requests

API_KEY = '6083081731:AAGTHb_vcXZ0ZHE1_t8bAT9kxI6mIJkZFUw'
WEATHER_API_KEY = 'a9d64e585f21ad027a586d4b39ac7145'

print ('Bot started')


def handle_message(update , context):
     text = str(update.message.text).lower()
     print (message.chat.username + ' : ' + text)

     if text == 'help':
          update.message.reply_text (f"Hello {update['message']['chat']['first_name']}. This is a weather update bot designed by Barath for the coding task given by AST Consulting. \nHere are some commands to get you started with: \n\n'get  <City Name/Zip Code>': Type this command to get instant weather report of specified city/zip code \n'subscribe  <City Name/Zip Code>': Type this command to subscribe to this weather update bot to get regular weather updates on your specified city/zip code. \n'view': Type this command to view your weather update subscriptions.")

     elif text.startswith('get'):
          if len(text) <= 3:
               update.message.reply_text ("Invalid command. To get weather update type 'get  <City Name/Zip Code>'")
          else :
               city = text[4::]
               weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={WEATHER_API_KEY}")
               if (weather_data.json()['cod'] == '404'):
                    update.message.reply_text ("City Name/Zip Code is Invalid!")
               else:
                    update.message.reply_text (f"City : {weather_data.json()['name']} \nWeather : {weather_data.json()['weather'][0]['main']} \n\nTemperature : {weather_data.json()['main']['temp']} \nFeels Like : {weather_data.json()['main']['feels_like']} \nMinimum Temperature : {weather_data.json()['main']['temp_min']} \nMaximum Temperature : {weather_data.json()['main']['temp_max']} \n\nPressure : {weather_data.json()['main']['pressure']} \nHumidity : {weather_data.json()['main']['humidity']} \nWind Speed : {weather_data.json()['wind']['speed']}")
                    #print (f"City : {weather_data.json()['name']} \nWeather : {weather_data.json()['weather'][0]['main']} \n\nTemperature : {weather_data.json()['main']['temp']} \nFeels Like : {weather_data.json()['main']['feels_like']} \nMinimum Temperature : {weather_data.json()['main']['temp_min']} \nMaximum Temperature : {weather_data.json()['main']['temp_max']} \n\nPressure : {weather_data.json()['main']['pressure']} \nHumidity : {weather_data.json()['main']['humidity']} \nWind Speed : {weather_data.json()['wind']['speed']}")
     
     elif text.startswith('subscribe'):
          if len(text) <= 9:
               update.message.reply_text ("Invalid command. To subscribe to weather update bot type 'subscribe  <City Name/Zip Code>'")
          else:
               city = text[10::]
               weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={WEATHER_API_KEY}")
               if (weather_data.json()['cod'] == '404'):
                    update.message.reply_text ("City Name/Zip Code is Invalid!")
               else:
                    city_name = weather_data.json()['name']
                    flag = Subscribers.objects.filter(username=update.message.chat.username)
                    if flag.exists():
                         if flag.filter(city=city_name).exists():
                              update.message.reply_text (f"You have already subscribed to Weather Updates for {city_name}! Type 'view' to view your subscriptions")
                         else:
                              Subscribers.objects.create(username=update.message.chat.username, city=city_name, chat_id=update['message']['chat']['id'])
                              update.message.reply_text (f"Subscribed to Weather Updates for the city {city_name}")
                    else:
                         Subscribers.objects.create(username=update.message.chat.username, city=city_name, chat_id=update['message']['chat']['id'])
                         update.message.reply_text (f"Subscribed to Weather Updates for the city {city_name}")
               
     elif text == 'view':
          subscriptions = Subscribers.objects.filter(username=update.message.chat.username)
          if subscriptions.exists():
               message = ""
               for sub in subscriptions:
                    message += f"City : {sub.city} \nSubscribed on : {sub.subscribed_at} \n\n"
          else:
               message = "You have no weather update subscriptions"
          update.message.reply_text (message)
     
     elif text.startswith('unsubscribe'):
          if len(text) <= 11:
               update.message.reply_text ("Invalid command. To unsubscribe a city weather update type 'unsubscribe  <City Name/Zip Code>'")
          else:
               city = text[12::]
               weather_data = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&APPID={WEATHER_API_KEY}")
               subscription = Subscribers.objects.get(username=update.message.chat.username, city=weather_data.json()['name'])
               if subscription:
                    subscription.delete()
                    update.message.reply_text (f"City {weather_data.json()['name']} unsubscribed from your subscriptions. To view other subscriptions type 'view'")
               else:
                    update.message.reply_text (f"City {weather_data.json()['name']} is not in your subscription list. To view your subscriptions type 'view'")

     else:
          update.message.reply_text (f"Hi, {update['message']['chat']['first_name']}. Type 'help' to get started.")

if __name__ == '__main__':
     updater = Updater(API_KEY, use_context=True)
     dp = updater.dispatcher
     dp.add_handler(MessageHandler(Filters.text, handle_message))
     updater.start_polling()
     updater.idle()
