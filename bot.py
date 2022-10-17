import random
from datetime import datetime

import telebot
from telebot import types  # кнопки

import compliments
import config

bot = telebot.TeleBot(config.token)


def get_markup():
    """
        функция которая возвращает кнопку в телеграмм-канале
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("❤Получить приятность")
    markup.add(btn)
    return markup


def find_text(chat_id: int):
    """
    Определяем какой текст будет отправлен
    """
    values = compliments.all_values()
    size: int = len(values)
    rnd_index = -1
    now = datetime.now()
    if chat_id not in user_dict:
        user_dict[chat_id] = {"date": now.date(), "hour": now.hour, "count": 0, "list": list()}
    local_obj = user_dict[chat_id]
    local_list = local_obj["list"]
    if len(local_list) == size:
        local_list.clear()

    if now.date() != local_obj["date"] or local_obj["hour"] != now.hour:
        local_obj["count"] = 0

    if local_obj["count"] == 5:
        return f'Дорогая, ты прекрасна, на текущий момент ты уже получила приястностей, пора поделать дела😉 ' \
               '(Возвращайся чуть позже ❤)'

    while rnd_index < 0 or local_list.count(rnd_index) != 0:
        rnd_index = random.randrange(size)

    local_list.append(rnd_index)
    local_obj["count"] += 1

    return values[rnd_index]


@bot.message_handler(commands=['start'])
def start(message):
    """
    стартовое сообщение
    """
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     text="Привет, {}, тут ты можешь получить информацию о тебе ;)".format(
                         message.from_user.first_name),
                     reply_markup=get_markup()
                     )
    user_dict[chat_id] = list()
    # bot.send_message(message.from_user.id, compliments.text_message())


@bot.message_handler(content_types=['text'])
def send_message(message):
    """
    когда бот уже активно принимает сообщения
    """
    chat_id = message.chat.id
    message_text = find_text(chat_id)
    if message.text == "❤Получить приятность":
        bot.send_message(chat_id, message_text, reply_markup=get_markup())


bot.polling(none_stop=True, interval=0)
