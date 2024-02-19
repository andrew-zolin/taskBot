from datetime import datetime
import re
import zoneinfo
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from usefull_func import generateCode, try_del_message
from database_handler import DataBase
from temp_data import UserState
from config import *


bot = Bot(BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = DISABLE_WEB_PAGE_PREVIWE)
db = DataBase()
us = UserState()


async def joinWorkSpace_step1_message(message: types.Message):
    await try_del_message(message, bot)

    us.updateUserState(message.chat.id, 'joinWorkSpace')

    await message.answer(
        text = '📝 Enter workspace code:'
    )


async def joinWorkSpace_step2_message(message: types.Message):
    # await try_del_message(message, bot)

    try:
        work_space_code = message.text
        work_space_id = db.getWorkSpaceIdFromCode(work_space_code)
        if work_space_id == None:
            await message.answer(
                text = '❌ Incorrect code, please try again'
            )
            return None
        else: work_space_id = work_space_id[0] 
        work_space_name = db.getWorkSpaceInfoFromId(work_space_id)[1]
        row_info = db.getAllWorkSpaceInfoFromChatIdAndWorkSpaceId(message.chat.id, work_space_id)
        if row_info == None:
            db.addWorkSpacePartisipant(work_space_name, message.chat.id, work_space_id)
            await message.answer(
                text = f'''💠 You have joined the "{work_space_name}" workspace. 

⚡ You can get all your work spaces on /my_workspace command.''',
            )
        else:
            await message.answer(
                text = f'''✅ You have already joined at the "{work_space_name}" workspace.''',
            )
        us.dropUserState(message.chat.id)
    except Exception as e:
        print(e)


async def createWorkSpace_step1_message(message: types.Message):
    await try_del_message(message, bot)

    us.updateUserState(message.chat.id, 'createWorkSpace')

    await message.answer(
        text = '📝 Enter workspace name:'
    )


async def createWorkSpace_step2_message(message: types.Message):
    await try_del_message(message, bot)
    us.dropUserState(message.chat.id)
    workSpaceName = message.text

    allCodes = db.getAllWorkSpaceCodes()

    newWorkSpaceCode = generateCode()
    while newWorkSpaceCode in allCodes:
        newWorkSpaceCode = generateCode()

    try:
        work_space_names_list = db.getAllWorkSpaceNames()
        if workSpaceName not in work_space_names_list:
            db.addWorkSpace(workSpaceName, newWorkSpaceCode)
            _id = db.getWorkSpaceId(workSpaceName)
            db.addWorkSpacePartisipant(workSpaceName, message.chat.id, _id, 1)
        else:
            await message.answer(
                text = '❌ This name is taken, please try again'
            )
            return None
    except Exception as e:
        print(e)

    await message.answer(
        text = '''💠 Work space has been created.

⚡ You can get all your work spaces on /my_workspace command.'''
    )


async def workSpaceMenu(call: types.CallbackQuery):
    await try_del_message(call.message, bot)
    workSpaceId = call.data
    print(workSpaceId)
    workSpaceInfo = db.getWorkSpaceInfoFromId(workSpaceId)
    print(workSpaceInfo)
    is_admin = bool(db.getIsAdminWorkSpacePartisipant(call.message.chat.id, workSpaceId)[0])
    markup = InlineKeyboardMarkup(row_width = 2)
    if is_admin:        
        markup.add(InlineKeyboardButton(text = 'Create task', callback_data = f'create_task:{workSpaceId}'))
        markup.add(
            InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{workSpaceId}'),
            InlineKeyboardButton(text = 'Get meetings', callback_data = f'get_meeting:{workSpaceId}'),
        )
        markup.add(InlineKeyboardButton(text = 'Create meeting', callback_data = f'create_meeting:{workSpaceId}'))
        markup.add(InlineKeyboardButton(text = 'Exit and delete', callback_data = f'delete_ws:{workSpaceId}'))

    else:
        markup.add(
            InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{workSpaceId}'),
            InlineKeyboardButton(text = 'Get meetings', callback_data = f'get_meeting:{workSpaceId}'),
        )
        markup.add(InlineKeyboardButton(text = 'Exit', callback_data = f'exit_ws:{workSpaceId}'))

    leaderChatId = db.getLeaderWorkSpace(workSpaceId)[0]
    leaderName = db.getFirstNameFromChatId(leaderChatId)[0]
    workSpaceName = workSpaceInfo[1]
    referalLink = TEMPLATE_REFERAL_LINK.replace('ID', workSpaceInfo[2])

    await bot.send_photo(
        chat_id = call.message.chat.id,
        photo = open(f'{MEDIA_PATH}image/workSpace.png', 'rb'),
        caption = f'''💠 Name: "{workSpaceName}"
├ Leader: "{leaderName}"
└ Referal Link: `{referalLink}`
''',    
        parse_mode = 'markdown',
        reply_markup = markup,
    )

async def exitWorkSpaceMenu(call: types.CallbackQuery): 
    await try_del_message(call.message, bot)
    work_space_id = call.data.split(':')[1] 
    db.dropWorkSpacePartisipant(call.message.chat.id, work_space_id)
    await bot.send_message(
        chat_id = call.message.chat.id,
        text = '''💠 You have left the workspace.

⚡ You can get all your workspaces on /my_workspace command.
''',
    )

async def deleteWorkSpaceMenu(call: types.CallbackQuery): 
    await try_del_message(call.message, bot)
    work_space_id = call.data.split(':')[1] 
    db.cascadeDropWorkSpacePartisipant(work_space_id)
    db.dropWorkSpace(work_space_id)
    await bot.send_message(
        chat_id = call.message.chat.id,
        text = '''💠 Workspace has been deleted.

⚡ You can get all your workspaces on /my_workspace command.
''',
    )

# Create task
async def createTaskStep1(call: types.CallbackQuery):
    await try_del_message(call.message, bot)
    
    work_space_id = call.data.split(':')[1] 
    all_chat_id = db.getAllChatIdFromWorkSpaceParticipant(work_space_id)
    all_chat_id =  tuple([str(c[0]) for c in all_chat_id])
    responsible_user_name_list = 'All users'
    print('\n', all_chat_id, '\n')
    
    if call.data.split(':')[0] == 'addResp':
        responsible_user = int(call.data.split(':')[2])
        responsible_user_list = us.getRespUser(call.message.chat.id)
        responsible_user_list.append(responsible_user)
        responsible_user_name_list = db.getUserInfoFromManyId(tuple(responsible_user_list))
        print(responsible_user_name_list)
        responsible_user_name_list = ', '.join([i[1] for i in responsible_user_name_list])[0:] if responsible_user_name_list != None else 'All users'
        us.updateRespUser(call.message.chat.id, responsible_user_list)
        all_chat_id = tuple(filter(lambda x: int(x) not in responsible_user_list, all_chat_id))

    
    users_info = db.getUserInfoFromManyId(all_chat_id)
    markup = InlineKeyboardMarkup(row_width = 2)
    if users_info != None:
        markup.add(*[InlineKeyboardButton(text = first_name, callback_data = f'addResp:{work_space_id}:{_id}') for _id, first_name in users_info])
    markup.add(
        InlineKeyboardButton(text = 'Accept', callback_data = f'acceptResp:{work_space_id}'),
        InlineKeyboardButton(text = 'Cancel', callback_data = f'cencelResp:{work_space_id}'),
    )

    await bot.send_message(
        chat_id = call.message.chat.id,
        text = f'''📝 Select all responsible people for this task:

⚡ Responsible users: {responsible_user_name_list}        
''',
        reply_markup = markup,
    )
    us.updateUserState(call.message.chat.id, f'create_task_1:{work_space_id}')

async def createTaskStep2(call: types.CallbackQuery):
    await try_del_message(call.message, bot)
    work_space_id = call.data.split(':')[1] 

    await bot.send_message(
        chat_id = call.message.chat.id,
        text = '📝 Enter task description:'
    )
    us.updateUserState(call.message.chat.id, f'create_task_2:{work_space_id}')

async def createTaskStep3(message: types.Message):
    await try_del_message(message, bot)
    work_space_id = us.getUserState(message.chat.id).split(':')[1] 
    us.updateUserState(message.chat.id, f'create_task_3:{work_space_id}')
    us.updateTaskData(message.chat.id, message.text)
    
    await bot.send_message(
        chat_id = message.chat.id,
        text = """📝 Enter task end date time in format "01.01.2024 12:00"."""
    )
    
async def createTaskStep4(message: types.Message):
    # await try_del_message(message, bot)
    pattern = r'\b\d{2}.\d{2}.\d{4} \d{2}:\d{2}'
    print(re.match(pattern, message.text))
    if re.match(pattern, message.text) == None:
        await message.answer(
            text = '❌ Incorrect input date time, please try again.'
        )
        return None

    work_space_id = us.getUserState(message.chat.id).split(':')[1]
    responsible_users_list = us.getRespUser(message.chat.id)
    if responsible_users_list == []: 
        responsible_users_list = list(map(lambda x: x[0], db.getAllChatIdFromWorkSpaceParticipant(work_space_id)))
    print(responsible_users_list)
    responsible_users = ':'.join(map(str, responsible_users_list))[0:] 
    description = us.getTaskData(message.chat.id)
    time_create = datetime.now(zoneinfo.ZoneInfo("Asia/Tashkent")).strftime("%d.%m.%Y %H:%M")
    time_end = message.text

    db.addTask(description, responsible_users, time_create, time_end, work_space_id)
    task_id = db.getLastTaskFromWorkSpaceId(work_space_id = work_space_id)[-1]
    await bot.send_message(
        chat_id = message.chat.id,
        text = '''💠 Task has been created.''',
    )

    for _id in responsible_users_list:
        if message.chat.id == int(_id):
            continue
        await bot.send_message(
            chat_id = int(_id),
            text = f"""<b>Task id:</b> <em>{task_id}.</em>

<b>Describe:</b> <em>{description}.</em>

<b>Time end:</b> <em>{time_end}.</em>
""" 
        )

    us.dropUserState(message.chat.id)
    us.dropTaskData(message.chat.id)
    us.dropRespUser(message.chat.id)


async def cencelResp(call: types.CallbackQuery):
    await try_del_message(call.message, bot)

    await bot.send_message(
        chat_id = call.message.chat.id,
        text = '❌ You have canceled task creation.',
    )
    workSpaceId = call.data.split(':')[1]
    call.data = workSpaceId 
    await workSpaceMenu(call)
    