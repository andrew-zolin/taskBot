from aiogram import Bot
# from usefull_func import Singleton

class Config:

    with open('../tokens.txt', 'r') as f:
        token_list = f.readlines()
    TEST_TOKEN = token_list[0].split('==')[1].replace('\n', '')
    MAIN_TOKEN = token_list[1].split('==')[1].replace('\n', '')

    BOT_TOKEN = TEST_TOKEN

    DISABLE_WEB_PAGE_PREVIWE = False

    TEMPLATE_REFERAL_LINK: str = 'https://t.me/USERNAME?start=ID'

    SCHEDULE_TASK_1: int = 60 #Time in seconds
    SCHEDULE_TASK_2: int = 30 #Time in seconds

    DATABASE_PATH = '../webApp/db.sqlite3'
    LOGGING_PATH = '../logging/log.txt'
    MEDIA_PATH = '../webApp/media/'

    @classmethod
    async def updateRefLink(cls, bot: Bot):
        username = await bot.get_me()
        username = username['username']
        print(f'\nBot name: {username}\n')
        # global TEMPLATE_REFERAL_LINK 
        cls.TEMPLATE_REFERAL_LINK = cls.TEMPLATE_REFERAL_LINK.replace('USERNAME', username)
        print(f'\nTEMPLATE_REFERAL_LINK: {cls.TEMPLATE_REFERAL_LINK}\n')


config = Config()