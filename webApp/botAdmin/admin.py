from django.contrib import admin
from .models import *
from .forms import *

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'first_name',)
    form = UserForm

@admin.register(WorkSpace)
class WorkSpaceAdmin(admin.ModelAdmin):
    list_display = ('work_space_name', 'work_space_code')
    form = WorkSpaceForm

@admin.register(WorkSpacePartisipant)
class WorkSpacePartisipantAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'is_admin', 'work_space',)
    form = WorkSpacePartisipantForm

@admin.register(WorkSpaceTask)
class WorkSpaceTaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'responsible_users', 'description', 'time_create', 'time_end', 'work_space',)
    form = WorkSpaceTaskForm
    
@admin.register(WorkSpaceMeeting)
class WorkSpacemeetingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'invite_link', 'work_space',)
    form = WorkSpaceMeetingForm
