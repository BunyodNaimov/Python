from datetime import datetime

import telebot
from telebot import custom_filters
from telebot.types import BotCommand, ReplyKeyboardRemove
from environs import Env

from keyboards import share_phone_btn, save_inline_btn, \
    get_languages_btn, get_program_language_btn
from messages import messages
from states import StudentRegistrationForm
from task import Chat, Task, Save
from utils import get_fullname, write_row_to_csv, get_language_code_by_chat_id

env = Env()
env.read_env()

BOT_TOKEN = env("TELEGRAM_API")

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="html")


# /start
@bot.message_handler(commands=["start"])
def welcome_message(message):
    chat_id = message.chat.id
    user = message.from_user
    fullname = get_fullname(user.first_name, user.last_name)
    bot.send_message(chat_id, f"Assalomu alaykum, {fullname}", reply_markup=get_languages_btn("register"))


@bot.callback_query_handler(lambda call: call.data.startswith("register_language_"))
def set_language_query_handler(call):
    message = call.message
    lang_code = call.data.split("_")[2]
    chat = message.chat
    new_chat = Chat(
        chat.id,
        get_fullname(chat.first_name, chat.last_name),
        lang_code
    )
    write_row_to_csv(
        "chats.csv",
        list(new_chat.get_attrs_as_dict().keys()),
        new_chat.get_attrs_as_dict()
    )

    bot.delete_message(chat.id, message.id)
    bot.send_message(chat.id, messages[lang_code].get("add_task"))


@bot.message_handler(commands=["register"])
def register_student_handler(message):
    bot.send_message(message.chat.id, "Ismingizni kiriting")
    bot.set_state(message.from_user.id, StudentRegistrationForm.first_name, message.chat.id)


@bot.message_handler(state=StudentRegistrationForm.first_name)
def first_name_get(message):
    bot.send_message(message.chat.id, "Familyangizni kiriting")
    bot.set_state(message.from_user.id, StudentRegistrationForm.last_name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["first_name"] = message.text


@bot.message_handler(state=StudentRegistrationForm.last_name)
def last_name_get(message):
    bot.send_message(message.chat.id, "Telefon raqamingizni kiriting", reply_markup=share_phone_btn)
    bot.set_state(message.from_user.id, StudentRegistrationForm.phone, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["last_name"] = message.text


@bot.message_handler(state=StudentRegistrationForm.phone, content_types=["contact", "text"])
def phone_get(message):
    bot.send_message(message.chat.id, "Yoshingizni kiriting", reply_markup=ReplyKeyboardRemove())
    bot.set_state(message.from_user.id, StudentRegistrationForm.age, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.contact is None:
            data["phone"] = message.text

        else:
            data["phone"] = message.contact.phone_number


@bot.message_handler(state=StudentRegistrationForm.age)
def age_get(message):
    bot.send_message(message.chat.id, "Tilni kiriting:", reply_markup=get_languages_btn("lang"))
    bot.set_state(message.from_user.id, StudentRegistrationForm.language, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data["age"] = message.text


@bot.callback_query_handler(lambda call: call.data.startswith("lang"), state=StudentRegistrationForm.language)
def language_get(call):
    message = call.message
    lang_code = call.data.split("_")[2]
    bot.send_message(message.chat.id, 'Kursni kiriting:', reply_markup=get_program_language_btn("course"))
    bot.set_state(message.from_user.id, StudentRegistrationForm.course, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['language'] = lang_code


@bot.callback_query_handler(lambda call: call.data.startswith("course"), state=StudentRegistrationForm.course)
def course_get(call):
    message = call.message
    course = call.data.split("_")[1]
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['course'] = course
        msg = "Quyidagi ma'lumotlar qa'bul qilindi:\n"
        msg += f"Fullname: {data.get('first_name')} {data.get('last_name')}\n"
        msg += f"Phone: {data.get('phone')}\n"
        msg += f"Age: {data.get('age')}\n"
        msg += f"Language: {data.get('language')}\n"
        msg += f"Course: {data.get('course')}"
        bot.send_message(message.chat.id, msg, parse_mode="html", reply_markup=save_inline_btn("save"))
    bot.delete_state(message.from_user.id, message.chat.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("save"))
def callback(call):
    message = call.message
    text = call.data.split("_")[1]
    if text == "ok":
        save_info = Save(
            text[0].split(":")[1].strip(),
            text[1].split(":")[1].strip(),
            text[2].split(":")[1].strip(),
            text[3].split(":")[1].strip(),
            text[4].split(":")[1].strip(),
        )
        write_row_to_csv(
            "registration.csv",
            save_info.get_save_info_csv().keys(),
            save_info.get_save_info_csv()
        )
    elif text == "no":
        bot.send_message(message.chat.id, "Ma'lumotlar saqlanmadi qaytadan /register")


# /add
@bot.message_handler(commands=["add"])
def add_task_handler(message):
    chat_id = message.chat.id
    lang_code = get_language_code_by_chat_id(chat_id, "chats.csv")
    msg = messages[lang_code].get("send_task")
    bot.send_message(message.chat.id, msg)

    bot.register_next_step_handler(message, get_task_handler)


@bot.message_handler(content_types=["text"])
def get_task_handler(message):
    chat_id = message.chat.id
    if message.content_type != "text":
        bot.send_message(chat_id, "Invalid format.")

    new_task = Task(chat_id, message.text, datetime.now())
    write_row_to_csv(
        "tasks.csv",
        list(new_task.get_attrs_as_dict().keys()),
        new_task.get_attrs_as_dict()
    )

    bot.send_message(chat_id, "Add successfully.")


def my_commands():
    return [
        BotCommand("/start", "Start bot"),
        BotCommand("/add", "Add new task"),
        BotCommand("/register", "Register student")
    ]


bot.add_custom_filter(custom_filters.StateFilter(bot))

if __name__ == "__main__":
    print("Started...")
    bot.set_my_commands(commands=my_commands())
    bot.infinity_polling()
