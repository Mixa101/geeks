from aiogram import executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from fsm_store import register_store_handlers
from decouple import config
from db import db_main


TOKEN = config('BOT_TOKEN') # получаем токен бота через decouple

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage()) # создаем диспетчер и кэш

register_store_handlers(dp) # регистрируем обработчики

async def on_startup(_):
    await db_main.sql_create()


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup) # запускаем бота