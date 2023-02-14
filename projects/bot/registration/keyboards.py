from datetime import datetime

from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def get_languages_btn(action):
    languages = {
        "UZ 🇺🇿": "uz",
        "RU 🇷🇺": "ru",
        "ENG 🇬🇧": "en"
    }

    languages_inline_btn = InlineKeyboardMarkup()

    languages_inline_btn.add(
        InlineKeyboardButton(
            list(languages.keys())[0], callback_data=f"{action}_language_{list(languages.values())[0]}"
        ),
        InlineKeyboardButton(
            list(languages.keys())[1], callback_data=f"{action}_language_{list(languages.values())[1]}"
        ),
        InlineKeyboardButton(
            list(languages.keys())[2], callback_data=f"{action}_language_{list(languages.values())[2]}"
        )
    )
    return languages_inline_btn


def save_inline_btn(action):
    save = {
        "☑️": "ok",
        "✏️": "no"
    }
    save_btn = InlineKeyboardMarkup()

    save_btn.add(
        InlineKeyboardButton(list(save.keys())[0], callback_data=f"{action}_{list(save.values())[0]}"),
        InlineKeyboardButton(list(save.keys())[1], callback_data=f"{action}_{list(save.values())[1]}")
    )
    return save_btn


def get_program_language_btn(action):
    program_btn = {
        "Python": "Python",
        "C++": "C++",
        "C#": "C#"
    }

    languages_program_btn = InlineKeyboardMarkup()

    languages_program_btn.add(
        InlineKeyboardButton(list(program_btn.keys())[0],
                             callback_data=f"{action}_{list(program_btn.values())[0]}"),
        InlineKeyboardButton(list(program_btn.keys())[1],
                             callback_data=f"{action}_{list(program_btn.values())[1]}"),
        InlineKeyboardButton(list(program_btn.keys())[2],
                             callback_data=f"{action}_{list(program_btn.values())[2]}")
    )
    return languages_program_btn


share_phone_btn = ReplyKeyboardMarkup(resize_keyboard=True)
share_phone_btn.add(KeyboardButton("Share phone", request_contact=True))
