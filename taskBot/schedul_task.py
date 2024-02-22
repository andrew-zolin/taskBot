from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from config import config
import zoneinfo
import asyncio
import pytz


bot = Bot(config.BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = config.DISABLE_WEB_PAGE_PREVIWE)


async def sendReminder(message: types.Message, responsible_users_list, task_id, description, time_create, time_end):
    print('\nFunc <sendReminder> work\n')

    for _id in responsible_users_list:
        await bot.send_message(
            chat_id = int(_id),
            text = f""" ⚡ <b>Reminder about task</b>
├ <b>Task id:</b> <em>{task_id}.</em>

├ <b>Describe:</b> <em>{description}.</em>

├ <b>The time of ending:</b> <em>{time_end.strftime("%d.%m.%Y %H:%M")}.</em>
└ <b>The time of creating:</b> <em>{time_create}.</em>
""",
        )

async def sendReminderTask(message: types.Message, responsible_users_list, task_id, description, time_create, time_end): 
    date_time: datetime = time_end # "01.01.2024 12:00"
    
    # Вычислить время ожидания до наступления назначенного времени
    current_time: datetime = datetime.now()
    current_time: datetime = current_time.astimezone(zoneinfo.ZoneInfo("Asia/Tashkent"))
    date_time: datetime    = date_time.astimezone(zoneinfo.ZoneInfo("Asia/Tashkent"))
    print(date_time, current_time, sep='\n')

    time_to_wait = (date_time - current_time).total_seconds()
    
    if time_to_wait > 0:
        print(f'\nTask has been created\n')
        await asyncio.sleep(time_to_wait)
        await sendReminder(message, responsible_users_list, task_id, description, time_create, time_end)







