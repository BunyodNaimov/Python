from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

days_btn = {
    "Weather for 5 days": "5"
}

days_inline_btn = InlineKeyboardMarkup()

days_inline_btn.add(
    InlineKeyboardButton(list(days_btn.keys())[0], callback_data=list(days_btn.values())[0])
)
