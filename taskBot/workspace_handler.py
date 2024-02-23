from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, executor
from aiogram.utils.markdown import hide_link
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from schedul_task import sendReminderTask
from command_handler import start_command
from usefull_func import callAlertFucnInDev, generateCode, try_del_message, try_del_message_from_ids
from database_handler import DataBase
from temp_data import UserState
from config import config
import zoneinfo
import re


bot = Bot(config.BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = config.DISABLE_WEB_PAGE_PREVIWE)
db = DataBase()
us = UserState()


async def get_my_workspaces_callback(call: types.CallbackQuery):
    us.updateUserState(call.message.chat.id, 'my_workspace')

    markup = InlineKeyboardMarkup(row_width = 2)
    nameList = db.getWorkSpaceNamesAndIdFromUser(call.message.chat.id)
    print(nameList)
    if nameList != None:
        markup.add(*[InlineKeyboardButton(text = name, callback_data = _id) for _id, name in nameList])
    markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_start'))

    msg = await call.message.edit_caption(
        caption = '⚡ Your work spaces:',
        reply_markup = markup,
    )

    message_ids = us.getMessagesToDelete(call.message.chat.id)
    message_ids.append(msg)
    us.updateMessagesToDelete(call.message.chat.id, message_ids)


async def joinWorkSpace_step1_message(message: types.Message):
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)
    
    us.updateUserState(message.chat.id, 'joinWorkSpace')

    msg = await message.answer(
        text = '📝 Enter workspace code:'
    )
    message_ids = us.getMessagesToDelete(message.chat.id)
    message_ids.append(msg.message_id)
    us.updateMessagesToDelete(message.chat.id, message_ids)

async def joinWorkSpace_step2_message(message: types.Message):
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)

    try:
        work_space_code = message.text
        work_space_id = db.getWorkSpaceIdFromCode(work_space_code)
        if work_space_id == None:
            msg = await message.answer(
                text = '❌ Incorrect code, please try again'
            )
            message_ids = us.getMessagesToDelete(message.chat.id)
            message_ids.append(msg.message_id)
            us.updateMessagesToDelete(message.chat.id, message_ids)
            return None
        else: work_space_id = work_space_id[0] 
        work_space_name = db.getWorkSpaceInfoFromId(work_space_id)[1]
        row_info = db.getAllWorkSpaceInfoFromChatIdAndWorkSpaceId(message.chat.id, work_space_id)
        if row_info == None:
            db.addWorkSpacePartisipant(work_space_name, message.chat.id, work_space_id)
#            
            print(work_space_id)
            workSpaceInfo = db.getWorkSpaceInfoFromId(work_space_id)
            print(workSpaceInfo)
            is_admin = bool(db.getIsAdminWorkSpacePartisipant(message.chat.id, work_space_id)[0])
            markup = InlineKeyboardMarkup(row_width = 2)
            if is_admin:        
                markup.add(InlineKeyboardButton(text = 'Create task', callback_data = f'create_task:{work_space_id}'))
                markup.add(
                    InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{work_space_id}'),
                    InlineKeyboardButton(text = 'Join meeting', callback_data = f'join_meeting:{work_space_id}'),
                )
                markup.add(InlineKeyboardButton(text = 'Exit and delete', callback_data = f'delete_ws:{work_space_id}'))
            else:
                markup.add(
                    InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{work_space_id}'),
                    InlineKeyboardButton(text = 'Join meeting', callback_data = f'join_meeting:{work_space_id}'),
                )
                markup.add(InlineKeyboardButton(text = 'Exit', callback_data = f'exit_ws:{work_space_id}'))
            markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_ws_catalog'))

            leaderChatId = db.getLeaderWorkSpace(work_space_id)[0]
            leaderName = db.getFirstNameFromChatId(leaderChatId)[0]
            workSpaceName = workSpaceInfo[1]
            referalLink = config.TEMPLATE_REFERAL_LINK.replace('ID', workSpaceInfo[2])

            msg = await bot.send_photo(
                chat_id = message.chat.id,
                photo = open(f'{config.MEDIA_PATH}image/workSpace.png', 'rb'),
                caption = f'''💠 Space Name: "{workSpaceName}"
        ├  Leader: "{leaderName}"
        └  Referal Link: `{referalLink}`
        ''',    
                parse_mode = 'markdown',
                reply_markup = markup,
            )

        else:
            msg = await message.answer(
                text = f'''✅ You have already joined at the "{work_space_name}" workspace.''',
            )
            message_ids = us.getMessagesToDelete(message.chat.id)
            message_ids.append(msg.message_id)
            us.updateMessagesToDelete(message.chat.id, message_ids)
        us.dropUserState(message.chat.id)
    except Exception as e:
        print(e)


async def createWorkSpace_step1_message(message: types.Message):
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)

    us.updateUserState(message.chat.id, 'createWorkSpace')

    msg = await message.answer(
        text = '📝 Enter workspace name:'
    )
    us.updateMessagesToDelete(message.chat.id, [msg.message_id])

async def createWorkSpace_step2_message(message: types.Message):
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
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
            workSpaceId = db.getWorkSpaceId(workSpaceName)
            db.addWorkSpacePartisipant(workSpaceName, message.chat.id, workSpaceId, 1)
        else:
            msg = await message.answer(
                text = '❌ This name is taken, please try again'
            )
            message_ids = us.getMessagesToDelete(message.chat.id)
            message_ids.append(msg.message_id)
            us.updateMessagesToDelete(message_ids)
            return None
    except Exception as e:
        print(e)

    print(workSpaceId)
    workSpaceInfo = db.getWorkSpaceInfoFromId(workSpaceId)
    print(workSpaceInfo)
    is_admin = bool(db.getIsAdminWorkSpacePartisipant(message.chat.id, workSpaceId)[0])
    markup = InlineKeyboardMarkup(row_width = 2)
    if is_admin:        
        markup.add(InlineKeyboardButton(text = 'Create task', callback_data = f'create_task:{workSpaceId}'))
        markup.add(
            InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{workSpaceId}'),
            InlineKeyboardButton(text = 'Join meeting', callback_data = f'join_meeting:{workSpaceId}'),
        )
        markup.add(InlineKeyboardButton(text = 'Exit and delete', callback_data = f'delete_ws:{workSpaceId}'))
    else:
        markup.add(
            InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{workSpaceId}'),
            InlineKeyboardButton(text = 'Join meeting', callback_data = f'join_meeting:{workSpaceId}'),
        )
        markup.add(InlineKeyboardButton(text = 'Exit', callback_data = f'exit_ws:{workSpaceId}'))
    markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_ws_catalog'))

    leaderChatId = db.getLeaderWorkSpace(workSpaceId)[0]
    leaderName = db.getFirstNameFromChatId(leaderChatId)[0]
    workSpaceName = workSpaceInfo[1]
    referalLink = config.TEMPLATE_REFERAL_LINK.replace('ID', workSpaceInfo[2])

    await bot.send_photo(
        chat_id = message.chat.id,
        photo = open(f'{config.MEDIA_PATH}image/workSpace.png', 'rb'),
        caption = f'''💠 Space Name: "{workSpaceName}"
├  Leader: "{leaderName}"
└  Referal Link: `{referalLink}`
''',    
        parse_mode = 'markdown',
        reply_markup = markup,
    )


async def workSpaceMenu(call: types.CallbackQuery, back = False):
    await try_del_message(call.message, bot)
    workSpaceId = call.data
    if back:
        workSpaceId = call.data.split(':')[1]

    print(workSpaceId)
    workSpaceInfo = db.getWorkSpaceInfoFromId(workSpaceId)
    print(workSpaceInfo)
    is_admin = bool(db.getIsAdminWorkSpacePartisipant(call.message.chat.id, workSpaceId)[0])
    markup = InlineKeyboardMarkup(row_width = 2)
    if is_admin:        
        markup.add(InlineKeyboardButton(text = 'Create task', callback_data = f'create_task:{workSpaceId}'))
        markup.add(
            InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{workSpaceId}'),
            InlineKeyboardButton(text = 'Join meeting', callback_data = f'join_meeting:{workSpaceId}'),
        )
        markup.add(InlineKeyboardButton(text = 'Exit and delete', callback_data = f'delete_ws:{workSpaceId}'))
    else:
        markup.add(
            InlineKeyboardButton(text = 'Get tasks', callback_data = f'get_task:{workSpaceId}'),
            InlineKeyboardButton(text = 'Join meeting', callback_data = f'join_meeting:{workSpaceId}'),
        )
        markup.add(InlineKeyboardButton(text = 'Exit', callback_data = f'exit_ws:{workSpaceId}'))
    markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_ws_catalog'))

    leaderChatId = db.getLeaderWorkSpace(workSpaceId)[0]
    leaderName = db.getFirstNameFromChatId(leaderChatId)[0]
    workSpaceName = workSpaceInfo[1]
    referalLink = config.TEMPLATE_REFERAL_LINK.replace('ID', workSpaceInfo[2])

    msg = await bot.send_photo(
        chat_id = call.message.chat.id,
        photo = open(f'{config.MEDIA_PATH}image/workSpace.png', 'rb'),
        caption = f'''💠 Space Name: "{workSpaceName}"
├  Leader: "{leaderName}"
└  Referal Link: `{referalLink}`
''',    
        parse_mode = 'markdown',
        reply_markup = markup,
    )

    message_ids = us.getMessagesToDelete(call.message.chat.id)
    message_ids.append(msg.message_id)
    us.updateMessagesToDelete(message_ids)

async def exitWorkSpaceMenu(call: types.CallbackQuery): 
    await try_del_message(call.message, bot)
    work_space_id = call.data.split(':')[1] 
    db.dropWorkSpacePartisipant(call.message.chat.id, work_space_id)
    
    await start_command(call.message, True)

async def deleteWorkSpaceMenu(call: types.CallbackQuery): 
    await try_del_message(call.message, bot)
    work_space_id = call.data.split(':')[1] 
    db.deleteTasksFromWorkSpaceId(work_space_id)
    db.cascadeDropWorkSpacePartisipant(work_space_id)
    db.dropWorkSpace(work_space_id)
  
    await start_command(call.message, True)
    
# Create task
async def createTaskStep1(call: types.CallbackQuery):
    message_ids = us.getMessagesToDelete(call.message.chat.id)
    await try_del_message_from_ids(call.message, bot, message_ids)
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

    msg = await bot.send_message(
        chat_id = call.message.chat.id,
        text = '📝 Enter task description:'
    )
    message_ids = us.getMessagesToDelete(call.message.chat.id)
    message_ids.append(msg.message_id)
    us.updateMessagesToDelete(call.message.chat.id, message_ids)
    us.updateUserState(call.message.chat.id, f'create_task_2:{work_space_id}')

async def createTaskStep3(message: types.Message):
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)

    work_space_id = us.getUserState(message.chat.id).split(':')[1] 
    us.updateUserState(message.chat.id, f'create_task_3:{work_space_id}')
    us.updateTaskData(message.chat.id, message.text)
    
    msg = await bot.send_message(
        chat_id = message.chat.id,
        text = """📝 Enter task end date time in format "01.01.2024 12:00"."""
    )
    message_ids = us.getMessagesToDelete(message.chat.id)
    message_ids.append(msg.message_id)
    us.updateMessagesToDelete(message.chat.id, message_ids)
    
async def createTaskStep4(message: types.Message) -> None:
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)

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

    for _id in responsible_users_list:
        if message.chat.id == int(_id):
            continue
        await bot.send_message(
            chat_id = int(_id),
            text = f"""💠 <b>Task id:</b> <em>{task_id}.</em>
├  <b>Responsible users:</b> {responsible_users}

├  <b>Description:</b> {description}.

└  <b>Deadline:</b> <em>{time_end}.</em>
""" 
        )

    # =====================================================================================================

    tasks = db.getAllTaskFromWorkSpaceId(work_space_id)
    print(tasks)

    us.updateTaskContainer(message.chat.id, tasks)
    is_admin = bool(db.getIsAdminWorkSpacePartisipant(message.chat.id, work_space_id)[0])
    current_pos = 0
    len_pos = len(tasks)

    task_id = tasks[current_pos][0]
    description = tasks[current_pos][1]
    responsible_user_name_list = tasks[current_pos][2].split(':')
    responsible_user_name_list = db.getUserInfoFromManyId(tuple(responsible_user_name_list))
    responsible_users = ', '.join([i[1] for i in responsible_user_name_list])[0:]
    time_create = tasks[current_pos][3]
    time_end = tasks[current_pos][4]

    markup = InlineKeyboardMarkup(row_width = 3)
    if is_admin:
        markup.add(
            InlineKeyboardButton(text = 'Delete', callback_data = f'delete_t:{work_space_id}:{task_id}'),
            # InlineKeyboardButton(text = 'Update', callback_data = f'update_t:{work_space_id}:{task_id}'),
        )
    markup.add(
        InlineKeyboardButton(text = '<', callback_data = f'<:{work_space_id}'),     
        InlineKeyboardButton(text = f'{current_pos+1}/{len_pos}', callback_data = '...'),        
        InlineKeyboardButton(text = '>', callback_data = f'>:{work_space_id}'),      
    )
    markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_ws_manu:{work_space_id}'))

    text = f'''💠 <b>Task id:</b> <em>{task_id}</em>
├  <b>Responsible users:</b> <em>{responsible_users}</em>

├  <b>Description:</b> {description}

└  <b>Deadline:</b> <em>{time_end}</em>'''

    await try_del_message(message, bot)
    await bot.send_message(
        chat_id = message.chat.id,
            text = text,
            reply_markup = markup,
        ) 

    us.dropUserState(message.chat.id)
    us.dropTaskData(message.chat.id)
    us.dropRespUser(message.chat.id)

    us.updateUserState(message.chat.id, f'{current_pos}:{work_space_id}')

    date_time: datetime = datetime.strptime(time_end, "%d.%m.%Y %H:%M")
    # first_date = date_time - timedelta(hours=3)
    first_date: datetime = date_time - timedelta(seconds = config.SCHEDULE_TASK_1)
    second_date: datetime = date_time - timedelta(seconds = config.SCHEDULE_TASK_2)
    third_date: datetime = date_time
    await sendReminderTask(message, responsible_users_list, task_id, description, time_create, first_date)
    await sendReminderTask(message, responsible_users_list, task_id, description, time_create, second_date)
    await sendReminderTask(message, responsible_users_list, task_id, description, time_create, third_date)

    

async def cencelResp(call: types.CallbackQuery):
    await try_del_message(call.message, bot)

    await bot.send_message(
        chat_id = call.message.chat.id,
        text = '❌ You have canceled task creation.',
    )
    workSpaceId = call.data.split(':')[1]
    call.data = workSpaceId 
    await workSpaceMenu(call)
    

async def getTask(call: types.CallbackQuery, update = False, diraction = None, back = False):
    work_space_id = call.data.split(':')[1]
    if back:
        work_space_id = us.getUserState(call.message.chat.id).split(':')[1]
    tasks = db.getAllTaskFromWorkSpaceId(work_space_id)
    print(tasks)
    if tasks == None or tasks == []:
        await call.answer(
            text = '❌ You have`t any tasks.'
        )
        return None

    us.updateTaskContainer(call.message.chat.id, tasks)
    is_admin = bool(db.getIsAdminWorkSpacePartisipant(call.message.chat.id, work_space_id)[0])
    current_pos = 0
    len_pos = len(tasks)

    if update:
        current_pos = int(us.getUserState(call.message.chat.id).split(':')[0])

    match diraction:
        case diraction if diraction == '<': 
            if current_pos > 0: current_pos -= 1
            else: return None
        case diraction if diraction == '>': 
            if current_pos < len_pos-1: current_pos += 1
            else: return None

    

    task_id = tasks[current_pos][0]
    description = tasks[current_pos][1]
    responsible_user_name_list = tasks[current_pos][2].split(':')
    responsible_user_name_list = db.getUserInfoFromManyId(tuple(responsible_user_name_list))
    responsible_users = ', '.join([i[1] for i in responsible_user_name_list])[0:]
    time_create = tasks[current_pos][3]
    time_end = tasks[current_pos][4]

    markup = InlineKeyboardMarkup(row_width = 3)
    if is_admin:
        markup.add(
            InlineKeyboardButton(text = 'Delete', callback_data = f'delete_t:{work_space_id}:{task_id}'),
            # InlineKeyboardButton(text = 'Update', callback_data = f'update_t:{work_space_id}:{task_id}'),
        )
    markup.add(
        InlineKeyboardButton(text = '<', callback_data = f'<:{work_space_id}'),     
        InlineKeyboardButton(text = f'{current_pos+1}/{len_pos}', callback_data = '...'),        
        InlineKeyboardButton(text = '>', callback_data = f'>:{work_space_id}'),      
    )
    markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_ws_manu:{work_space_id}'))

    text = f'''💠 <b>Task id:</b> <em>{task_id}</em>
├  <b>Responsible users:</b> <em>{responsible_users}</em>

├  <b>Description:</b> {description}

└  <b>Deadline:</b> <em>{time_end}</em>'''

    if update:
        await call.message.edit_text(
                text = text,  
                reply_markup = markup,
            ) 
    else:
        await try_del_message(call.message, bot)
        await bot.send_message(
            chat_id = call.message.chat.id,
                text = text,
                reply_markup = markup,
            ) 
    us.updateUserState(call.message.chat.id, f'{current_pos}:{work_space_id}')


async def checkDelOrNoTask(call: types.CallbackQuery):
    work_space_id = call.data.split(':')[1]
    task_id = call.data.split(':')[2]

    markup = InlineKeyboardMarkup(row_width = 2)
    markup.add(
        InlineKeyboardButton(text = 'Delete', callback_data = f'ap_del_t:{work_space_id}:{task_id}'),
        InlineKeyboardButton(text = 'Cansel', callback_data = f'ca_del_t:{work_space_id}:{task_id}'),
    )

    await call.message.edit_text(
        text = '💠 Delete this task ?',
        reply_markup = markup,
    )

async def getChoiceDelOrNoTask(call: types.CallbackQuery):
    data = call.data.split(':')[0]
    work_space_id = call.data.split(':')[1]
    task_id = call.data.split(':')[2]
    us.updateUserState(call.message.chat.id, f'getTask:{work_space_id}')
    if data == 'ap_del_t':
        db.deleteTaskFromTaskId(task_id)
        await call.answer(
            text = '💠 Task has been deleted.',
        )
        
    else:
        await call.answer(
            text = '💠 Delting has been canseled.',
        )
    await getTask(call, back = True)


async def updateTask(call: types.CallbackQuery):
    await callAlertFucnInDev(call)


async def joinMeeting(call: types.CallbackQuery):

    await try_del_message(call.message, bot)

    work_space_id = call.data.split(':')[1]
    workSpaceInfo = db.getWorkSpaceInfoFromId(work_space_id)
    workSpaceName = workSpaceInfo[1] 
    leaderChatId = db.getLeaderWorkSpace(work_space_id)[0]
    leaderName = db.getFirstNameFromChatId(leaderChatId)[0]

    meeting_info = db.getMeetingFromWorkSpaceId(work_space_id)
    print(meeting_info)
    meeting = 'The link has not yet been created'
    if meeting_info != None:
        meeting_link = meeting_info[2]
        print(meeting_link)
        meeting = hide_link(meeting_link)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_t_m:{work_space_id}'))

    await bot.send_message(
        chat_id = call.message.chat.id,
        text = f'''💠 Space Name: "{workSpaceName}"

├ Leader: "{leaderName}"

{meeting}''', # └ Google meet link:
        reply_markup = markup,
    )

async def backTaskMenu(call: types.CallbackQuery):
    await getTask(call, back = True)