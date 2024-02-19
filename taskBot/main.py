from aiogram import Bot, Dispatcher, types, executor
from aiogram.types.message import ContentType
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from command_handler import *
from workspace_handler import *
from callback_handler import callback_handler
from message_handler import message_handler
from config import *
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = Bot(BOT_TOKEN, parse_mode="HTML", disable_web_page_preview = DISABLE_WEB_PAGE_PREVIWE)
dp = Dispatcher(bot)


@dp.message_handler(commands = 'start')
async def start(message: types.Message):
    await start_command(message)

@dp.message_handler(commands = 'my_workspace')
async def my_workspace(message: types.Message):
    await get_my_workspaces_command(message)

@dp.message_handler(commands = 'my_tasks')
async def my_tasks(message: types.Message):
    ...
    # await createWorkSpace_step1_message(message)

@dp.message_handler(commands = 'join_workspace')
async def join_workspace(message: types.Message):
    await joinWorkSpace_step1_message(message)

@dp.message_handler(commands = 'create_new')
async def create_new(message: types.Message):
    await createWorkSpace_step1_message(message)

@dp.message_handler()
async def message(message: types.Message):
    await message_handler(message)

@dp.callback_query_handler()
async def callback(call: types.CallbackQuery):
    await callback_handler(call)

# @dp.message_handler(commands = 'start')
# async def start(message: types.Message):
#     ...


if __name__ == '__main__':
    executor.start_polling(dp)