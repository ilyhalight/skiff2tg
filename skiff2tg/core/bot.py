from aiogram import Bot, Dispatcher

from core.settings import get_settings

settings = get_settings()
bot = Bot(token = settings.bot_token)
dp = Dispatcher(bot)