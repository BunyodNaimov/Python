from datetime import datetime
import telebot
from environs import Env
from telebot.types import BotCommand

from get_data import get_data
from keyboards import days_inline_btn

env = Env()
env.read_env()

BOT_TOKEN = env("TELEGRAM_API")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="html")


# /weather
@bot.message_handler(commands=["weather"])
def weather_handler(message):
    today = datetime.now()
    weather_data = get_data()
    today_weather = None
    for day_weather in weather_data:
        day_date = datetime.strptime(day_weather.get("day"), "%Y.%m.%d")
        if day_date.date() == today.date():
            today_weather = day_weather
    msg = f"<b>Bugungi ob-havo:</b>\n\n" \
          f"<i>Harorat:</i> {today_weather.get('average_temperature')}"
    bot.send_message(message.chat.id, msg, parse_mode="html", reply_markup=days_inline_btn)


@bot.callback_query_handler(func=lambda call: True)
def weather_handler(call):
    print(call.data)
    if "5" in call.data:
        day_weather_message(call.message)


@bot.message_handler(func=lambda message: message.text.startswith("Feb"))
def day_weather_message(message):
    date_msg = message.text
    date = datetime.strptime(date_msg, "%b %d %Y")
    weather_data = get_data()
    weather = None
    for day_weather in weather_data:
        day_date = datetime.strptime(day_weather.get("day"), "%Y.%m.%d")
        if day_date.date() == date.date():
            weather = day_weather
    msg = f"<b>{date_msg} ob-havo:</b>\n\n" \
          f"<i>Harorat:</i> {weather.get('average_temperature')}"
    print(msg)
    bot.reply_to(message, msg)


def my_commands():
    return [
        BotCommand("/weather", "Today weather")
    ]


if __name__ == "__main__":
    print("Started...")
    bot.set_my_commands(commands=my_commands())
    bot.infinity_polling()
