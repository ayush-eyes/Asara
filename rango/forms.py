from rango.models import UserProfile, Project, Comment, Task, Chat
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple, DateInput, Select
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password')
        widgets={
            }
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture','cv','mobile','dob','place','institute','department','gender')
        widgets={
            'department':Select(choices=UserProfile.DEPARTMENT_CHOICES,),
            'gender':Select(choices=UserProfile.GENDER_CHOICES,),
        }
        
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('project_name','project_description','project_department')
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('task_name','task_description','task_deadline')

class chatform(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('chat_message','chat_user')
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment_text','comment_file')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ('first_name','last_name','username','email')
