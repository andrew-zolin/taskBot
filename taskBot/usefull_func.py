from aiogram import Bot, types
from config import *
from string import digits, ascii_letters, punctuation
import datetime
import random

class Singleton(object):

    def __new__(cls, *args, **kwargs):
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        cls.__it__ = it = object.__new__(cls)
        it.init(*args, **kwargs)
        return it

    def init(self, *args, **kwargs):
        pass


async def try_del_message(message: types.Message, bot: Bot):
    try:
        await bot.delete_message(
            chat_id = message.chat.id,
            message_id = message.message_id,
        )
    except:
        pass


def generateCode(symbols = digits+ascii_letters, length = 16):
    return ''.join([random.choice(symbols) for _ in range(length)]) 
    

def errorLoger(func):
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res 
        except Exception as error:
            with open(LOGGING_PATH, 'r', encoding = 'UTF-8') as f:
                oldData = f.read()
            with open(LOGGING_PATH, 'w', encoding = 'UTF-8') as f:
                dateTime = str(datetime.datetime.now())
                errorMessage = f'''\n---------------------------
Имя функции: {func.__name__}
Ошибка: {str(error)}
Дата и время: {dateTime}
---------------------------\n
'''
                f.write(oldData + errorMessage)
            print(f"Имя функции: {func.__name__}, Ошибка: {str(error)}")
        return None
    return wrapper

