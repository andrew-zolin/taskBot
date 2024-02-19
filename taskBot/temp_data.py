
from usefull_func import Singleton


class UserState(Singleton):
    
    def init(self):
        super().__init__()
        self.__userState = {}
        self.__taskData = {}
        self.__respUser = {}


    # User state
    def getUserState(self, chat_id):
        return self.__userState.get(chat_id)

    def updateUserState(self, chat_id, state):
        self.__userState.update({chat_id: state})
    
    def dropUserState(self, chat_id):
        try:
            self.__userState.pop(chat_id)
        except Exception as e:
            print(e)
    
    # Task data
    def getTaskData(self, chat_id):
        return self.__taskData.get(chat_id)

    def updateTaskData(self, chat_id, data):
        self.__taskData.update({chat_id: data})
    
    def dropTaskData(self, chat_id):
        try:
            self.__taskData.pop(chat_id)
        except Exception as e:
            print(e)
    
    # Responsible users
    def getRespUser(self, chat_id) -> list:
        return self.__respUser.get(chat_id, [])

    def updateRespUser(self, chat_id, users):
        self.__respUser.update({chat_id: users})
    
    def dropRespUser(self, chat_id):
        try:
            self.__respUser.pop(chat_id)
        except Exception as e:
            print(e)
