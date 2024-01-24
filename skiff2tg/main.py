from aiogram import executor

from core.logger import init_logging
from core.events import on_startup, on_shutdown
from core.bot import dp
from scheluder import scheduler


if __name__ == '__main__':
    init_logging()
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)