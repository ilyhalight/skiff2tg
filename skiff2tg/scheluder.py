import logging
import aiogram.utils.markdown as md

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.settings import get_settings
from core.bot import bot
from skiff import get_last_threads

scheduler = AsyncIOScheduler()
logger = logging.getLogger(__name__)
settings = get_settings()
except_ids = []

async def schelude_new_threads():
    try:
        content: str|list = await get_last_threads()
    except Exception as err:
        logger.exception(err)
        content = md.text(
            f'An error occurred when requesting to {md.bold("skiff.com:")}',
            md.code(f'{err!r}'),
            sep = '\n\n'
        )

    if type(content) is list:
        messages: list = []
        for thread in content:
            labels = ', '.join([f'{label["labelName"]} ({label["variant"]})' for label in thread['attributes']['userLabels']])
            for email in thread['emails']:
                if email['scheduleSendAt'] != None:
                    continue

                timestamp = email['createdAt'] / 1000
                if timestamp < settings.min_timestamp:
                    continue

                if email['id'] in except_ids:
                    continue

                text_date = datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M:%S')

                precontent = md.text(
                    md.escape_md(f'New message from {email["from"]["address"]} ({email["from"]["name"]})'),
                    '',
                    f'{md.bold("Labels:")} {md.escape_md(labels)}',
                    f'{md.bold("Date:")} {md.escape_md(text_date)}',
                    f'{md.bold("Attachments:")} {len(email["attachmentMetadata"])}',
                    sep = '\n'
                )

                messages.append({
                    'id': email['id'],
                    'timestamp': timestamp,
                    'content': precontent
                })

        messages.sort(key=lambda x: x['timestamp'])
        for message in messages:
            await bot.send_message(settings.chat_id, message['content'], parse_mode='MarkdownV2')
            except_ids.append(message['id'])
    else:
        await bot.send_message(settings.chat_id, content, parse_mode='MarkdownV2') # type: ignore

scheduler.add_job(schelude_new_threads, 'interval', minutes=settings.scheluder_interval)