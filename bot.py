import telebot
from telebot import types

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


@bot.message_handler(commands=['start'])
def start(message):
    """
    стартовое сообщение
    """
    bot.send_message(message.chat.id,
                     text="Привет, {}, тут ты можешь получить информацию о тебе ;)".format(
                         message.from_user.first_name),
                     reply_markup=get_markup()
                     )
    # bot.send_message(message.from_user.id, compliments.text_message())

@bot.message_handler(content_types=['text'])
def send_message(message):
    """
    когда бот уже активно принимает сообщения
    """
    if message.text == "❤Получить приятность":
        bot.send_message(message.chat.id, compliments.text_message(), reply_markup=get_markup())


bot.polling(none_stop=True, interval=0)
