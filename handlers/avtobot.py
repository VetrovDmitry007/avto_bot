#
# Модуль автобота
#

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData
import main

cb_admin = CallbackData('pref', 'action', 'step')


def register_handlers(dp: Dispatcher):
    """
    Регистрация хендлеров
    :param dp:
    :return:
    """
    dp.register_message_handler(start, commands=['start'], state="*")
    # dp.register_callback_query_handler(ch_start, cb.filter(step=["start"]), state="*")


def register_handlers_final(dp: Dispatcher):
    """
    Регистрация хендлеров final
    :param dp:
    :return:
    """
    dp.register_message_handler(handler_txt, content_types=['text'], state="*")



# commands=['start'], state="*"
async def start(message: types.Message, state: FSMContext):
    await message.answer("Приветствуем!")


# content_types=['text'], state="*"
async def handler_txt(message: types.Message):
    await message.answer('Напишите /start')