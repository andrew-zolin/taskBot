from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from workspace_handler import *
from temp_data import UserState
from config import *


bot = Bot(BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = DISABLE_WEB_PAGE_PREVIWE)
us = UserState()


async def message_handler(message: types.Message):
    data = message.text

    match data:
        case 'My workspaces 🌝' : await ... # joinWorkSpace_step1_message(message)
        case 'Create new 🌚'    : await createWorkSpace_step1_message(message)
        case _ if us.getUserState(message.chat.id) == 'createWorkSpace': await createWorkSpace_step2_message(message)
        case _ if us.getUserState(message.chat.id) == 'joinWorkSpace': await joinWorkSpace_step2_message(message)
        case _ if us.getUserState(message.chat.id).split(':')[0] == 'create_task_2': await createTaskStep3(message)
        case _ if us.getUserState(message.chat.id).split(':')[0] == 'create_task_3': await createTaskStep4(message)
        

