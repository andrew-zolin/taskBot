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
        case data if data.split(':')[0] == 'create_task'            : await createTaskStep1(call)
        case data if data.split(':')[0] == 'addResp'                : await createTaskStep1(call)
        case data if data.split(':')[0] == 'get_task'               : await getTask(call)
        case data if data.split(':')[0] == '<'                      : await getTask(call, True, '<')
        case data if data.split(':')[0] == '>'                      : await getTask(call, True, '>')
        case data if data.split(':')[0] == 'delete_t'               : await checkDelOrNoTask(call)
        case data if data.split(':')[0] == 'acceptResp'             : await createTaskStep2(call)
        case data if data.split(':')[0] == 'cencelResp'             : await cencelResp(call)
        case data if data.split(':')[0] in ('ap_del_t', 'ca_del_t') : await getChoiceDelOrNoTask(call)
        case data if data.split(':')[0] == 'update_t'               : await updateTask(call)
        case data if data.split(':')[0] == 'exit_ws'                : await exitWorkSpaceMenu(call)
        case data if data.split(':')[0] == 'delete_ws'              : await deleteWorkSpaceMenu(call)
        case data if data.split(':')[0] == 'join_meeting'           : await joinMeeting(call)
        case data if data.split(':')[0] == 'back_t_m'               : await workSpaceMenu(call, back = True)
        case data if data.split(':')[0] == 'back_ws_manu'           : await workSpaceMenu(call, True)
        case data if us.getUserState(call.message.chat.id) == 'my_workspace': await workSpaceMenu(call)
        # case _ if us.getUserState(call.message.chat.id).split(':')[0] == 'create_task_2': await workSpaceMenu(call)