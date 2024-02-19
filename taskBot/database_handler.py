from usefull_func import *
from config import *
import sqlite3


class DataBase(Singleton):
    
    def init(self):
        super().__init__()
        self.db_path = DATABASE_PATH

    def __select(self, _select: tuple = None, _from: str = None, _where: dict = None, fetchall = False):
        with sqlite3.connect(self.db_path) as c:
            selectData = 'SELECT '
            selectData += '*' if _select == None else ''.join([f'{i}, ' for i in _select])[:-2] if isinstance(_select, tuple) else str(_select)
            fromData = ' ' if _from == None else f' FROM {_from} '
            whereData = ' ' if _where == None else 'WHERE ' + ''.join([f"{k} = '{i}' AND " for k, i in zip(_where.keys(), _where.values())])[:-4]
            if _where == None:   
                executeData = f'{selectData}{fromData}'
            else:
                executeData = f'{selectData}{fromData}{whereData}'
            print(f'\n{executeData}\n')
            res = c.execute(executeData)
        if fetchall:
            return res.fetchall()
        else:
            return res.fetchone()
    
    def __update(self, _update: str, _set: dict, _where: dict = None):
        with sqlite3.connect(self.db_path) as c:
            updateData = f"""UPDATE {_update} """
            setData = f"""SET {tuple(_set.keys())[0]} = '{tuple(_set.values())[0]}'"""
            whereData = f"""WHERE {tuple(_where.keys())[0]} = '{tuple(_where.values())[0]}'"""
            executeData = f'{updateData}{setData}{whereData}'
            print(f'\n{executeData}\n')
            c.execute(executeData)      
            c.commit()      
       
    def __insert(self, _insert: str, _values: dict):
        with sqlite3.connect(self.db_path) as c:
            executeData = f"""INSERT INTO {_insert} {tuple(_values.keys())} VALUES {tuple(_values.values())}"""
            print(f'\n{executeData}\n')
            c.execute(executeData)
            c.commit()
    
    def __delete(self, _from: str, _where: dict):
        with sqlite3.connect(self.db_path) as c:
            whereData = 'WHERE ' + ''.join([f"{k} = '{i}' AND " for k, i in zip(_where.keys(), _where.values())])[:-4]
            executeData = f"""DELETE FROM {_from} {whereData}"""
            print(f'\n{executeData}\n')
            c.execute(executeData)
            c.commit()
            

    # User handler
    def addUser(self, chat_id, first_name):
        self.__insert('user', {'chat_id': chat_id, 'first_name': first_name})

    def getFirstNameFromChatId(self, chat_id):
        return self.__select('first_name', 'user', {'chat_id': chat_id})

    def updateUserFirstName(self, chat_id, first_name):
        self.__update('user', {'first_name': first_name}, {'chat_id': chat_id})
    
    def getUserInfo(self, chat_id):
        return self.__select(_from = 'user', _where = {'chat_id': chat_id})

    def getUserInfoFromManyId(self, chat_ids: tuple):
        print('\n', chat_ids, '\n')
        with sqlite3.connect(self.db_path) as c:
            if len(chat_ids) == 1:
                executeData = f"""SELECT * FROM user WHERE chat_id = '{chat_ids[0]}'"""
            elif len(chat_ids) > 1:
                executeData = f"""SELECT * FROM user WHERE chat_id IN {chat_ids}"""
            else:
                return None
            print(f'\n{executeData}\n')
        return c.execute(executeData).fetchall()
    
    # Work space handler
    def addWorkSpace(self, workSpaceName, workSpaceCode):
        self.__insert('workSpace', {'work_space_name': workSpaceName, 'work_space_code': workSpaceCode})

    def dropWorkSpace(self, work_space_id):
        self.__delete('workSpace', {'id': work_space_id})

    def getAllWorkSpaceNames(self):
        names = self.__select('work_space_name', 'workSpace', fetchall = True)
        try:
            names = [c[0] for c in names]
            print(names)
            return names
        except Exception as e:
            print(e)
            return None
        
    def getWorkSpaceIdFromCode(self, work_space_code):
        return self.__select('id', 'workSpace', {'work_space_code': work_space_code})

    def getLeaderWorkSpace(self, workSpaceId):
        return self.__select('chat_id', 'workSpacePartisipant', {'work_space_id':workSpaceId})

    def getWorkSpaceInfo(self, workSpaceName):
        return self.__select(_from = 'workSpace', _where = {'work_space_name': workSpaceName})

    def getWorkSpaceId(self, workSpaceName):
        return self.__select('id', 'workSpace', {'work_space_name': workSpaceName})[0]

    def getWorkSpaceInfoFromId(self, workSpaceId):
        return self.__select(_from = 'workSpace', _where = {'id': workSpaceId})

    def getIsAdminWorkSpacePartisipant(self, chat_id, work_space_id):
        return self.__select('is_admin', 'workSpacePartisipant', {'chat_id': chat_id, 'work_space_id': work_space_id})

    def getAllWorkSpaceCodes(self):
        codeList = self.__select(_select = 'work_space_code', _from = 'workSpace', fetchall = True)
        try:
            codeList = [c[0] for c in codeList]
            print(codeList)
            return codeList
        except Exception as e:
            print(e)
            return None
                
    def addWorkSpacePartisipant(self, work_space_name, chat_id, work_space_id, is_admin = 0): 
        self.__insert('workSpacePartisipant', {'chat_id': chat_id, 'is_admin': is_admin, 'work_space_name': work_space_name, 'work_space_id': work_space_id})
    
    def dropWorkSpacePartisipant(self, chat_id, work_space_id): 
        self.__delete('workSpacePartisipant', {"chat_id": chat_id, 'work_space_id': work_space_id})

    def cascadeDropWorkSpacePartisipant(self, work_space_id):
        self.__delete('workSpacePartisipant', {'work_space_id': work_space_id})

    def getWorkSpaceNamesAndIdFromUser(self, chat_id):
        names = self.__select(('work_space_id', 'work_space_name'), 'workSpacePartisipant', {'chat_id': chat_id}, fetchall = True)
        return names

    def getAllWorkSpaceInfoFromChatIdAndWorkSpaceId(self, chat_id, work_space_id):
        return self.__select(_from = 'workSpacePartisipant', _where = {'chat_id': chat_id, 'work_space_id': work_space_id})

    def getAllChatIdFromWorkSpaceParticipant(self, work_space_id):
        return self.__select('chat_id', 'workSpacePartisipant', {'work_space_id': work_space_id}, True)

    # Task handler
    def addTask(self, responsible_users, description, time_create, time_end, work_space_id):
        self.__insert('workSpaceTask', {'responsible_users': responsible_users, 'description': description, 'time_create': time_create, 'time_end': time_end, 'work_space_id': work_space_id})

    def getLastTaskFromWorkSpaceId(self, work_space_id):
        row = self.__select('task_id', 'workSpaceTask', {'work_space_id': work_space_id}, fetchall = True)
        if row != None:
            return list(map(lambda x: x[0], row))
        


    # def getAllTasksDataFromWorkSpaceId(self, )

    def getAllTasksFromWorkSpaceId(self, work_space_id):
        return self.__select('task_id', 'workSpaceTask', {'work_space_id': work_space_id}, fetchall = True)

    def getTaskDataFromTaskId(self, task_id):
        return self.__select(_from = 'workSpaceTask', _where = {'task_id': task_id})
    
    def dropTask(self, task_id):
        self.__delete('workSpaceTask', {'task_id': task_id})