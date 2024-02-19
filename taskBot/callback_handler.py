from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from workspace_handler import *
from temp_data import UserState
from config import *


bot = Bot(BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = DISABLE_WEB_PAGE_PREVIWE)
us = UserState()


async def callback_handler(call: types.CallbackQuery):
    
    data = call.data
    match data:
        case data if data.split(':')[0] == 'create_task'    : await createTaskStep1(call)
        case data if data.split(':')[0] == 'addResp'        : await createTaskStep1(call)
        case data if data.split(':')[0] == 'get_task'       : await ...
        case data if data.split(':')[0] == 'get_meeting'    : await ...
        case data if data.split(':')[0] == 'create_meeting' : await ...
        case data if data.split(':')[0] == 'exit_ws'        : await exitWorkSpaceMenu(call)
        case data if data.split(':')[0] == 'delete_ws'      : await deleteWorkSpaceMenu(call)
        case data if data.split(':')[0] == 'acceptResp'     : await createTaskStep2(call)
        case data if data.split(':')[0] == 'cencelResp'     : await cencelResp(call)
        case _ if us.getUserState(call.message.chat.id) == 'my_workspace': await workSpaceMenu(call)
        # case _ if us.getUserState(call.message.chat.id).split(':')[0] == 'create_task_2': await workSpaceMenu(call)