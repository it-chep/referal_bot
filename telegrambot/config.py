from aiogram import Dispatcher, Bot
from maxim_referal.settings import BOT_TOKEN

bot = Bot(token=str(BOT_TOKEN))
dp = Dispatcher(bot)
