from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from database_handler import DataBase
from temp_data import UserState
from usefull_func import try_del_message
from config import *


bot = Bot(BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = DISABLE_WEB_PAGE_PREVIWE)
db = DataBase()
us = UserState()


async def start_command(message: types.Message):
    await try_del_message(message, bot)

    us.updateUserState(message.chat.id, 'start')

    userInfo = db.getUserInfo(message.chat.id)
    
    if userInfo == None:
        db.addUser(message.chat.id, message.chat.first_name)

    markup = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    markup.add(
        KeyboardButton(text = 'My workspaces 🌝'),
        KeyboardButton(text = 'Create new 🌚'),
    )

    await bot.send_photo(
        chat_id = message.chat.id,
        photo = open(f'{MEDIA_PATH}image/main.png', 'rb'),
        caption = f'''Hello {message.chat.first_name}''',
        reply_markup = markup,
    )

    if " " in message.text: 
        try:
            work_space_code = message.text.split()[1]
            work_space_id = db.getWorkSpaceIdFromCode(work_space_code)
            if work_space_id == None:
                await message.answer(
                    text = '❌ Incorrect code, please try again.'
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
        except Exception as e:
            print(e)
    
async def get_my_workspaces_command(message: types.Message):
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

async def get_my_tasks_command(message: types.Message):
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


