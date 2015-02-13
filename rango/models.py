from django.db import models
from django.contrib.auth.admin import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to='pic/%Y/%m/%d', null=True, blank=True)
    cv = models.FileField(upload_to='cv/%Y/%m/%d', null=True, blank=True)
    mobile = models.IntegerField(null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    place = models.CharField(max_length=50, null=True, blank=True)
    institute = models.CharField(max_length=50, null=True,blank=True)
    
    DEPARTMENT_CHOICES = (
        ('CSE','Computer Science'),
        ('EE','Electrical'),
        ('ME','Mechanical'),
    )
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, null=True, blank=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O','Transgender'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True,blank=True)

    def __unicode__(self):
        return str(self.user.username).replace(' ','_')

class Comment(models.Model):
    comment_user = models.ForeignKey(User)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_text = models.CharField(max_length=250, null=True, blank=True)
    comment_file = models.FileField(upload_to='task/%Y/%m/%d', null=True, blank=True)
    
    def __unicode__(self):
        return str(self.comment_user.username).replace(' ','_')
    
class Task(models.Model):
    task_member = models.ManyToManyField(User, blank=True, null=True)
    task_name = models.CharField(max_length=50)
    task_description = models.CharField(max_length=250)
    task_deadline = models.DateTimeField(null=True, blank=True)
    task_comment = models.ManyToManyField(Comment,blank=True, null=True)
    task_complete = models.BooleanField(default=False)
    
    def __unicode__(self):
        return str(self.task_name).replace(' ','_')
    
class Notification(models.Model):
    applicants = models.ManyToManyField(User, blank=True, null=True)

class Chat(models.Model):
    chat_message = models.CharField(max_length=200)
    chat_time = models.DateTimeField(auto_now_add=True)
    chat_user = models.ForeignKey(User)

class Project(models.Model):
    project_leader = models.ForeignKey(User, related_name="leader")
    project_name = models.CharField(max_length=50)
    project_description = models.CharField(max_length=250)
    project_members=models.ManyToManyField(User, null=True, blank=True)
    DEPARTMENT_CHOICES = (
        ('CSE','Computer Science'),
        ('EE','Electrical'),
        ('ME','Mechanical'),
        ('OTHERS','Others'),
    )
    project_department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    project_task = models.ManyToManyField(Task,blank=True, null=True)
    project_created = models.DateTimeField(auto_now_add=True)
    project_notification = models.OneToOneField(Notification, blank=True, null=True)
    project_chat=models.ManyToManyField(Chat,blank=True,null=True)
    
    def __unicode__(self):
        return str(self.project_leader.username).replace(' ','_') + "_" + str(self.project_name).replace(' ','_')
    