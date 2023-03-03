# Weather Update BOT

## Description

This telegram bot can be used to get the weather of a specified city instantly, or subscribe to a city weather forecast to get timely updates on the weather of the city. Single user can subscribe to multiple cities and the user can unsubscribe to any city if they wish to.

## Getting Started

### Installing
* Open terminal in your desired location of installation of local.
* Clone the repository.
```
git clone https://github.com/htarab-b/Weather_Update_Telegram_bot.git
```
* Create a virtual environment. (Optional)
```
python3 -m venv env
```
* Install the requirements for the project in the 'requirements.txt' file.
```
pip install -r requirements.txt
```

### Executing program
* Open VS Code or any IDE.
* Run 'bot.py' python file.
* Open new terminal and start the django server.
```
python manage.py runserver
```
* Open another new terminal, start the celery worker service.
```
celery -A weather_bot worker --loglevel=info
```
* Open another new terminal, start the beat service.
```
celery -A weather_bot beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

## Use Bot
To view the bot that is started in the server, Open telegram and access the bot's chat profile.

Telegram link to chatbot : t.me/weatherupdatescodingtask_bot

Or you can use the search bar in telegram to find the bot. Bot username : weatherupdatescodingtask_bot

## Help
Instructions on how to use the bot can be viewed by sending a 'help' message.

Django admin panel superuser :
> Username : admin <br>Password  : adminpassword
