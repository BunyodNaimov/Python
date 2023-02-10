from datetime import datetime
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from projects.bot.utils import get_weather_days

languages_btn = ReplyKeyboardMarkup(resize_keyboard=True)

LANGUAGES = {
    "UZ 🇺🇿": "uz",
    "RU 🇷🇺": "ru",
    "ENG 🇬🇧": "en"
}

languages_inline_btn = InlineKeyboardMarkup()

languages_inline_btn.add(
    InlineKeyboardButton(list(LANGUAGES.keys())[0], callback_data=f"language_{list(LANGUAGES.values())[0]}"),
    InlineKeyboardButton(list(LANGUAGES.keys())[1], callback_data=f"language_{list(LANGUAGES.values())[1]}"),
    InlineKeyboardButton(list(LANGUAGES.keys())[2], callback_data=f"language_{list(LANGUAGES.values())[2]}")
)

SAVE = {
    "☑️": "ok",
    "✏️": "no"
}

save_inline_btn = InlineKeyboardMarkup()

save_inline_btn.add(
    InlineKeyboardButton(list(SAVE.keys())[0], callback_data=list(SAVE.values())[0]),
    InlineKeyboardButton(list(SAVE.keys())[1], callback_data=list(SAVE.values())[1])
)

languages_program_btn = {
    "Python": "Python",
    "C++": "C++",
    "C#": "C#"
}

inline_languages_program_btn = InlineKeyboardMarkup()

inline_languages_program_btn.add(
    InlineKeyboardButton(list(languages_program_btn.keys())[0], callback_data=list(languages_program_btn.values())[0]),
    InlineKeyboardButton(list(languages_program_btn.keys())[1], callback_data=list(languages_program_btn.values())[1]),
    InlineKeyboardButton(list(languages_program_btn.keys())[2], callback_data=list(languages_program_btn.values())[2])
)

share_phone_btn = ReplyKeyboardMarkup(resize_keyboard=True)
share_phone_btn.add(KeyboardButton("Share phone", request_contact=True))

days_btn = ReplyKeyboardMarkup(row_width=True)

for day in get_weather_days():
    formatted_day = datetime.strptime(day, "%Y.%m.%d").strftime("%b %d %Y")
    days_btn.add(
        KeyboardButton(formatted_day)
    )
