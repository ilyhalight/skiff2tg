from core.settings import get_settings
from core.bot import bot

settings = get_settings()

async def on_startup(dp):
    await bot.send_message(settings.chat_id, '✅ Bot started')

async def on_shutdown(dp):
    await bot.send_message(settings.chat_id, '❗Bot is turned off')