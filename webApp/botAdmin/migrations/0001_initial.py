# Generated by Django 4.2 on 2024-02-13 19:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "chat_id",
                    models.IntegerField(
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID юзера",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(max_length=200, verbose_name="Имя юзера"),
                ),
            ],
            options={
                "verbose_name": "Юзера",
                "verbose_name_plural": "Юзеры",
                "db_table": "user",
            },
        ),
        migrations.CreateModel(
            name="WorkSpace",
            fields=[
                (
                    "id",
                    models.IntegerField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID команды",
                    ),
                ),
                (
                    "work_space_name",
                    models.CharField(
                        max_length=200, unique=True, verbose_name="Имя команды"
                    ),
                ),
                (
                    "work_space_code",
                    models.CharField(max_length=300, verbose_name="Код для вступления"),
                ),
            ],
            options={
                "verbose_name": "Команду",
                "verbose_name_plural": "Команды",
                "db_table": "workSpace",
            },
        ),
        migrations.CreateModel(
            name="WorkSpaceTask",
            fields=[
                (
                    "task_id",
                    models.IntegerField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID Задачи",
                    ),
                ),
                (
                    "responsible_users",
                    models.CharField(
                        max_length=1024, verbose_name="Отвественные юзеры"
                    ),
                ),
                (
                    "description",
                    models.TextField(max_length=1024, verbose_name="Описание задачи"),
                ),
                (
                    "time_create",
                    models.DateTimeField(verbose_name="Вермя создания задачи"),
                ),
                (
                    "time_end",
                    models.DateTimeField(verbose_name="Вермя создания задачи"),
                ),
                (
                    "work_space",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="botAdmin.workspace",
                    ),
                ),
            ],
            options={
                "verbose_name": "Задачу",
                "verbose_name_plural": "Задачи",
                "db_table": "workSpaceTask",
            },
        ),
        migrations.CreateModel(
            name="WorkSpacePartisipant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("chat_id", models.IntegerField(verbose_name="ID юзера")),
                (
                    "is_admin",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="0 - Не админ; 1 - Админ ",
                        verbose_name="Указатель на админа",
                    ),
                ),
                (
                    "work_space_name",
                    models.CharField(max_length=200, verbose_name="Имя команды"),
                ),
                (
                    "work_space",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="botAdmin.workspace",
                    ),
                ),
            ],
            options={
                "verbose_name": "Участника команды",
                "verbose_name_plural": "Участники команд",
                "db_table": "workSpacePartisipant",
            },
        ),
        migrations.CreateModel(
            name="WorkSpaceMeeting",
            fields=[
                (
                    "meeting_id",
                    models.IntegerField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID встречи",
                    ),
                ),
                (
                    "name",
                    models.CharField(max_length=200, verbose_name="Название встречи"),
                ),
                ("date", models.DateTimeField(verbose_name="Дата и время встречи")),
                (
                    "invite_link",
                    models.CharField(
                        max_length=300, verbose_name="Приглачительная сылка"
                    ),
                ),
                (
                    "work_space",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="botAdmin.workspace",
                    ),
                ),
            ],
            options={
                "verbose_name": "Встречу",
                "verbose_name_plural": "Встречи",
                "db_table": "workSpaceMeeting",
            },
        ),
    ]
