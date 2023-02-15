import telebot
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env("TELEGRAM_API")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="html")


# /start
@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "Salom")


if __name__ == "__main__":
    print("Started.....")
    bot.infinity_polling()
