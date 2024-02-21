from django import forms
from .models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        
        fields = (
            "chat_id",
            "first_name",
        )
        widgets = {
            "chat_id": forms.NumberInput,
            "first_name": forms.TextInput,
        }


class WorkSpaceForm(forms.ModelForm):
    class Meta:
        model = WorkSpace
        
        fields = (
            "work_space_name",
            "work_space_code",
        )
        widgets = {
            "work_space_name": forms.TextInput,
            "work_space_code": forms.TextInput,
        }


class WorkSpacePartisipantForm(forms.ModelForm):
    class Meta:
        model = WorkSpacePartisipant
        
        fields = (
            "chat_id",
            "is_admin",
            "work_space",
        )
        widgets = {
            "chat_id": forms.NumberInput,
            "is_admin": forms.NumberInput,
            "work_space": forms.NumberInput,
        }


class WorkSpaceTaskForm(forms.ModelForm):
    class Meta:
        model = WorkSpaceTask
        
        fields = (
            "task_id",
            "responsible_users",
            "description",
            "time_create",
            "time_end",
            "work_space",
        )
        widgets = {
            "task_id": forms.NumberInput,
            "responsible_users": forms.TextInput,
            "description": forms.Textarea,
            "time_create": forms.DateTimeInput,
            "time_end": forms.DateTimeInput,
            "work_space": forms.NumberInput,
        }


class WorkSpaceMeetingForm(forms.ModelForm):
    class Meta:
        model = WorkSpaceMeeting
        
        fields = (
            "name",
            "date",
            "invite_link",
            "work_space",
        )
        widgets = {
            "name": forms.TextInput,
            "date": forms.TextInput,
            "invite_link": forms.TextInput,
            "work_space": forms.NumberInput,
        }

