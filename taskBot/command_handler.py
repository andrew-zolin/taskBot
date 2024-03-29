from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from database_handler import DataBase
from temp_data import UserState
from usefull_func import try_del_message, try_del_message_from_ids
from config import config


bot = Bot(config.BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = config.DISABLE_WEB_PAGE_PREVIWE)
db = DataBase()
us = UserState()


async def start_command(message: types.Message, back = False):

    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)
    us.updateUserState(message.chat.id, 'start')
    
    userInfo = db.getUserInfo(message.chat.id)
    
    if userInfo == None:
        db.addUser(message.chat.id, message.chat.first_name)

    markup = InlineKeyboardMarkup(row_width = 2)
    markup.add(
        InlineKeyboardButton(text = 'My workspaces 🌝', callback_data = 'my_workspaces'),
        InlineKeyboardButton(text = 'Create new 🌚', callback_data = 'create_new_ws'),
    )

    msg = await bot.send_photo(
        chat_id = message.chat.id,
        photo = open(f'{config.MEDIA_PATH}image/main.png', 'rb'),
        caption = f'''⚡ Hello <em>"{message.chat.first_name}"</em>

💠 <b>TaskBot</b>:

├-   Your smart task manager. 
├-   Simplify your to-do lists, 
└-   stay organized effortlessly.''',
        reply_markup = markup,
    )
    us.updateMessagesToDelete(message.chat.id, [msg.message_id])
    if back: return None
    if " " in message.text: 
        try:
            message_ids = us.getMessagesToDelete(message.chat.id)
            await try_del_message_from_ids(message, bot, message_ids)
            work_space_code = message.text.split()[1]
            work_space_id = db.getWorkSpaceIdFromCode(work_space_code)
            if work_space_id == None:
                msg = await message.answer(
                    text = '❌ Incorrect code, please try again.'
                )
                old_messages_id = us.getMessagesToDelete(message.chat.id)
                old_messages_id.append(msg.message_id)
                us.updateMessagesToDelete(message.chat.id, old_messages_id)
                return None
            else: work_space_id = work_space_id[0] 
            work_space_name = db.getWorkSpaceInfoFromId(work_space_id)[1]
            row_info = db.getAllWorkSpaceInfoFromChatIdAndWorkSpaceId(message.chat.id, work_space_id)
            if row_info == None:
                db.addWorkSpacePartisipant(work_space_name, message.chat.id, work_space_id)
#                 msg = await message.answer(
#                     text = f'''💠 You have joined the "{work_space_name}" workspace. 
            

# ⚡ You can get all your work spaces on /my_workspace command.''',
#                 )
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
            old_messages_id = us.getMessagesToDelete(message.chat.id)
            old_messages_id.append(msg.message_id)
            us.updateMessagesToDelete(message.chat.id, old_messages_id)
        except Exception as e:
            print(e)
    
async def get_my_workspaces_command(message: types.Message):
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)

    us.updateUserState(message.chat.id, 'my_workspace')

    markup = InlineKeyboardMarkup(row_width = 2)
    nameList = db.getWorkSpaceNamesAndIdFromUser(message.chat.id)
    print(nameList)
    if nameList != None:
        markup.add(*[InlineKeyboardButton(text = name, callback_data = _id) for _id, name in nameList])
    markup.add(InlineKeyboardButton(text = 'Back', callback_data = f'back_start'))

    await message.answer(
        text = '⚡ Your work spaces:',
        reply_markup = markup,
    )

async def get_my_tasks_command(message: types.Message):
    message_ids = us.getMessagesToDelete(message.chat.id)
    await try_del_message_from_ids(message, bot, message_ids)
    await try_del_message(message, bot)

    us.updateUserState(message.chat.id, 'my_workspace')

    markup = InlineKeyboardMarkup(row_width = 2)
    nameList = db.getWorkSpaceNamesAndIdFromUser(message.chat.id)
    print(nameList)
    if nameList != None:
        markup.add(*[InlineKeyboardButton(text = name, callback_data = _id) for _id, name in nameList])
        
    await message.answer(
        text = '⚡ Your work spaces:',
        reply_markup = markup,
    )


