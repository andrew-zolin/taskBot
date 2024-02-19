from django.db import models
import datetime
# Create your models here.


class User(models.Model): 

    chat_id = models.IntegerField(
        primary_key = True,
        unique = True,
        verbose_name = 'ID юзера',
    )

    first_name = models.CharField(
        max_length = 200,
        verbose_name = 'Имя юзера',
    )


    def __str__(self):
        return f"#{self.chat_id} {self.first_name}"

    class Meta:
        db_table = 'user'
        verbose_name = 'Юзера'
        verbose_name_plural = 'Юзеры'


class WorkSpace(models.Model):

    id = models.IntegerField(
        unique = True,
        auto_created = True,
        primary_key = True,
        verbose_name = 'ID команды'
    )

    work_space_name = models.CharField(
        max_length = 200,
        unique = True,
        verbose_name = 'Имя команды',
    )

    work_space_code = models.CharField(
        max_length = 300,
        verbose_name = 'Код для вступления',
    )


    def __str__(self):
        return f"#{self.id} {self.work_space_name} {self.work_space_code}"
    
    class Meta:
        db_table = 'workSpace'
        verbose_name = 'Команду'
        verbose_name_plural = 'Команды'


class WorkSpacePartisipant(models.Model):

    chat_id = models.IntegerField(
        verbose_name = 'ID юзера',
    )

    is_admin = models.PositiveIntegerField(
        default = 0,
        verbose_name = 'Указатель на админа',
        help_text = '0 - Не админ; 1 - Админ '
    )

    work_space_name = models.CharField(
        max_length = 200,
        # unique = True,
        verbose_name = 'Имя команды',
    )

    work_space = models.ForeignKey(WorkSpace, on_delete = models.CASCADE) # Внешний ключ к таблице WorkSpace

    def __str__(self):
        return f"#{self.chat_id} {self.is_admin} {self.work_space_name} {self.work_space}"
    
    class Meta:
        db_table = 'workSpacePartisipant'
        verbose_name = 'Участника команды'
        verbose_name_plural = 'Участники команд'


class WorkSpaceTask(models.Model):

    task_id = models.IntegerField(
        unique = True,
        primary_key = True,
        auto_created = True,
        verbose_name = 'ID Задачи'
    )

    responsible_users = models.CharField(
        max_length = 1024,
        verbose_name = 'Отвественные юзеры',
    ) 

    description = models.TextField(
        max_length = 1024,
        verbose_name = 'Описание задачи',
    )

    time_create = models.DateTimeField(
        # default = datetime.datetime.now(),
        verbose_name = 'Вермя создания задачи',
    )

    time_end = models.DateTimeField(
        # default = datetime.datetime.now(),
        verbose_name = 'Вермя создания задачи',
    )

    work_space = models.ForeignKey(WorkSpace, on_delete = models.CASCADE) # Внешний ключ к таблице WorkSpace

    def __str__(self):
        return f'#{self.task_id} {self.responsible_users} {self.description} {self.time_create} {self.time_end} {self.work_space}'
    
    class Meta:
        db_table = 'workSpaceTask'
        verbose_name = 'Задачу'
        verbose_name_plural = 'Задачи'


class WorkSpaceMeeting(models.Model):
    meeting_id = models.IntegerField(
        unique = True,
        primary_key = True,
        auto_created = True,
        verbose_name = 'ID встречи'
    )

    name = models.CharField(
        max_length = 200,
        verbose_name = 'Название встречи',
    )

    date = models.DateTimeField(
        # default = datetime.datetime.now(),
        verbose_name = 'Дата и время встречи',
    )

    invite_link = models.CharField(
        max_length = 300,
        verbose_name = 'Приглачительная сылка',   
    )

    work_space = models.ForeignKey(WorkSpace, on_delete = models.CASCADE) # Внешний ключ к таблице WorkSpace

    def __str__(self):
        return f'#{self.meeting_id} {self.name} {self.date} {self.invite_link} {self.work_space}'
    
    class Meta:
        db_table = 'workSpaceMeeting'
        verbose_name = 'Встречу'
        verbose_name_plural = 'Встречи'

