from aiogram import executor, Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from fsm_store import register_store_handlers
from decouple import config

TOKEN = config('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

register_store_handlers(dp)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)