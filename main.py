from aiogram import executor
import logging
from config import dp, bot, admins
from handlers import commands, echo, quiz, game, FSM_reg
import asyncio
from db import db_main

async def on_startup(_):
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Бот запущен!')
        await db_main.sql_create()

async def on_shutdown(_):
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Бот отключен')

commands.register_handlers_commands(dp)
quiz.register_handlers_quiz(dp)
FSM_reg.register_fsm_handlers(dp)
game.register_game_handlers(dp)
echo.register_handler_echo(dp)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)