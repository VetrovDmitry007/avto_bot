#
# Модуль автобота
#
import os
import tempfile

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
import main
from lib.vinru import get_inf_avto

cb_avtobot = CallbackData('pref', 'action', 'step')

class StatusAvto(StatesGroup):
    str_num = State()
    phote_num = State()



def register_handlers(dp: Dispatcher):
    """
    Регистрация хендлеров
    :param dp:
    :return:
    """
    dp.register_message_handler(start, commands=['start'], state="*")
    dp.register_message_handler(download_photo, content_types=["photo"], state="*")
    dp.register_callback_query_handler(load_ph, cb_avtobot.filter(step=["load_ph"]), state="*")
    dp.register_callback_query_handler(ch_pars_num, cb_avtobot.filter(step=["ch_pars_num"]), state="*")
    dp.register_message_handler(get_info_avt, state=StatusAvto.str_num)



def register_handlers_final(dp: Dispatcher):
    """
    Регистрация хендлеров final
    :param dp:
    :return:
    """
    dp.register_message_handler(handler_txt, content_types=['text'], state="*")


# commands=['start'], state="*"
async def start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Это автобот. Я могу по номеру авто вывести инфу об этой машине.")
    await get_num(message, state)



async def get_num(message: types.Message, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup()
    ls_action = ['Фотокамера', 'Клавиатура']
    ls_btn = []
    for action in ls_action:
        btn = types.InlineKeyboardButton(text=action, callback_data=cb_avtobot.new(action=action, step='load_ph'))
        ls_btn.append(btn)
    keyboard.add(*ls_btn)
    question = 'Укажите номер автомобиля при помощи фотокамеры или с помощью клавиатуры.'
    await message.answer(text=question, reply_markup=keyboard)


# cb_avtobot.filter(step=["load_ph"]), state="*"
async def load_ph(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # обработчик -- подтверждение ввода номера
    if callback_data["action"] == 'Фотокамера':
        await call.message.answer("Нажмите на скрепку и сделайти фото")
        # await StatusAvto.phote_num.set()
    else:
        await call.message.answer("Ведите номер с клавиатуры.")
        await StatusAvto.str_num.set()


# state=StatusAvto.str_num
async def get_info_avt(message: types.Message, state: FSMContext):
    # Ввод номера с клавиатуры
    # await message.answer(f"Введён номер: {message.text}")
    await state.update_data(str_num=message.text)
    await ch_num(message, state)


# content_types=["photo"], state="*"
async def download_photo(message: types.Message, state: FSMContext):
    # создаем временный файл
    fd, path = tempfile.mkstemp(suffix='.jpg', text=True, dir='./tmp/photos')
    await state.update_data(path_photo=path)
    await state.update_data(fd_photo=fd)
    # сохраняем фото в каталоге
    await message.photo[-1].download(destination_file=path)
    await message.answer("Распознование номера ...")
    await pars_num(message, state)


async def pars_num(message: types.Message, state: FSMContext):
    # 1. Распознаёт на фотографии авто изображение его номер
    state_dc = await state.get_data()
    arr_num = main.pa.get_number(state_dc['path_photo'])
    # print(arr_num)
    # 2. Читаем номер по фото
    str_avt_num = main.obj_num.pars_numb(arr_num)
    await state.update_data(str_num=str_avt_num)
    await ch_num(message, state)



async def ch_num(message: types.Message, state: FSMContext):
    # Проверка на правильность номера
    state_dc = await state.get_data()
    keyboard = types.InlineKeyboardMarkup()
    ls_action = ['Верно', 'Ошибка']
    ls_btn = []
    for action in ls_action:
        btn = types.InlineKeyboardButton(text=action, callback_data=cb_avtobot.new(action=action, step='ch_pars_num'))
        ls_btn.append(btn)
    keyboard.add(*ls_btn)
    question = f'Номер: {state_dc["str_num"]}'
    await message.answer(text=question, reply_markup=keyboard)


# cb_avtobot.filter(step=["ch_pars_num"]), state="*"
async def ch_pars_num(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    # обработчик -- подтверждение ввода номера
    state_dc = await state.get_data()
    if callback_data["action"] == 'Верно':
        # Получаем информацию с vinru.ru
        await call.message.answer("Поиск данных в базе ...")
        info_avto = get_inf_avto(state_dc['str_num'])
        await call.message.answer(info_avto)
        # Очистка хранилищя
        await state.finish()
        await get_num(call.message, state)
    else:
        await call.message.answer("Переснемите или ведите номер с клавиатуры.")
        await StatusAvto.str_num.set()
    # Удаление временного файла
    if state_dc.get('fd_photo', 0) > 0:
        await delTemFile(state_dc['fd_photo'], state_dc['path_photo'])


async def delTemFile(fd, path):
    # закрываем дескриптор файла
    os.close(fd)
    # уничтожаем файл
    os.unlink(path)


# content_types=['text'], state="*"
async def handler_txt(message: types.Message):
    await message.answer('Напишите /start')


