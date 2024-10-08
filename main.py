from aiogram import executor
import logging
from config import dp, bot
from handlers import commands, echo, quiz, game, FSM_reg

commands.register_handlers_commands(dp)
quiz.register_handlers_quiz(dp)
FSM_reg.register_fsm_handlers(dp)
game.register_game_handlers(dp)
echo.register_handler_echo(dp)

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)