# Telegram weather bot

The **[bot](https://github.com/kdudarev/task_controller)** helps to find out the weather in any city in the world. The site displays all registered users, from where you can send the weather to a specific user.

### Technology Stack:
- **[Python](https://www.python.org/)** - programming language (3.9.6)
- **[Aiogram](https://docs.aiogram.dev/en/latest/)** - asynchronous framework for Telegram Bot API (2.20)
- **[PostgreSQL](https://www.postgresql.org/)** - object-relational database system (PostgreSQL 14)
- **[Django](https://www.djangoproject.com/)** - Python Web framework (4.0.4)
- **[HTML](https://html.com/)** - markup language (HTML5)
- **[Bootstrap](https://getbootstrap.com/)** - HTML, CSS and JavaScript framework (django-bootstrap-v5==1.0.11)

# Installation

**1. Clone this repository:**
```
git clone https://github.com/kdudarev/telegram_weather_bot_with_django.git
```
**2. Change SECRET_KEY in settings.py:**
```
SECRET_KEY = "Your Secret Key"
```
**3. Add your bot token and weather API token to .env file:**
```
BOT_TOKEN = "Your bot token"
WEATHER_TOKEN = 'Your API key'
```
**4. Change DATABASES in settings.py to yours or use the example:**
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
**5. Change the database in bot/db.py if you are not using PostgreSQL:**
```
self.connection = "Your database".connect()
```
**6. Use virtual environment to install requirements:**
```
pip install -r requirements.txt
```
**7. Run the migration:**
```
python manage.py migrate
```
**8. Start the bot:**
```
python main_bot.py
```
**9. Start the server:**
```
python manage.py runserver
```
