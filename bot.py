import asyncio
import random
from datetime import datetime

# telebot
from telebot.async_telebot import AsyncTeleBot
import telebot
from telebot import types  # кнопки

import compliments
import config

bot = AsyncTeleBot(config.token)
user_dict = {}


class User:
    def __init__(self, city):
        # self.city = city
        keys = ["time", "compliment_id"]

        for key in keys:
            self.key = None


@bot.message_handler(commands=['start'])
async def start(message):
    """
        стартовое сообщение
    """
    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           text="Привет, {}, тут ты можешь получить информацию о тебе ;)".format(
                               message.from_user.first_name),
                           reply_markup=get_markup()
                           )
    now = datetime.now()
    user_dict[chat_id] = {"date": now.date(), "hour": now.hour, "count": 0, "list": list()}


@bot.message_handler(func=lambda message: message.text == "❤Получить приятность")
async def send_message(message):
    """
        когда бот уже активно принимает сообщения
    """
    chat_id = message.chat.id
    message_text = get_text_message(chat_id)
    await bot.send_message(chat_id, message_text, reply_markup=get_markup())


def get_markup():
    """
        функция которая возвращает кнопку в телеграмм-канале
    """
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("❤Получить приятность")
    markup.add(btn)
    return markup


def get_text_message(chat_id: int, param: bool = False):
    """
       Определяем какой текст будет отправлен
    """
    print(f"get_text_message {chat_id}")
    now = datetime.now()
    clean_object = {"date": now.date(), "hour": now.hour, "count": 0, "list": list()}

    values = compliments.all_values()
    size = len(values)
    rnd_index = -1

    if chat_id not in user_dict:
        user_dict[chat_id] = dict.copy(clean_object)
    local_obj = user_dict[chat_id]
    local_list = local_obj["list"]

    if len(local_list) == size:
        local_list.clear()

    if local_obj["date"] != now.date() or local_obj["hour"] != now.hour:
        local_obj.copy(clean_object)

    if local_obj["count"] >= 5 and not param:
        return f'Дорогая, ты прекрасна, на текущий момент ты уже получила приятностей, пора поделать дела😉' \
               '(Возвращайся чуть позже ❤)'

    while rnd_index < 0 or values[rnd_index] in local_list:
        rnd_index = random.randint(0, size - 1)

    local_list.append(values[rnd_index])
    local_obj["count"] += 1
    return values[rnd_index]


async def send_on_time():
    print(f"send_on_time")
    while True:
        # second = random.randrange(15)
        await asyncio.sleep(60*10)
        if (datetime.now().hour == 11) or (
                datetime.now().hour == 17):
            # for chat_id in user_dict:
            await bot.send_message(5141887105, get_text_message(5141887105, True), reply_markup=get_markup())
            print(f"Отправили сообщение в чат: {5141887105}")
        print(f"Отправка по времени, {datetime.now()}")


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    tasks = [
        loop.create_task(bot.polling()),
        loop.create_task(send_on_time()),
    ]
    wait_tasks = asyncio.wait(tasks)
    loop.run_until_complete(wait_tasks)
    loop.close()
