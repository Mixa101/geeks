from aiogram import Dispatcher, Bot
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

admins = ['645903918']
token = config('BOT_TOKEN')
bot = Bot(token=token)
dp = Dispatcher(bot, storage=MemoryStorage())