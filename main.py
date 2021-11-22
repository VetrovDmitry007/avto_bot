import asyncio
import setup
import logging
from handlers import avtobot
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from lib.parsavto import ParsaAvto
from lib.recogn import AvtoNum

bot = Bot(token=setup.token)
dp = Dispatcher(bot, storage=MemoryStorage())

pa = ParsaAvto()
obj_num = AvtoNum()

async def main():
    logging.basicConfig(level=logging.INFO)

    avtobot.register_handlers(dp)
    avtobot.register_handlers_final(dp)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())