from django.contrib import admin
from rango.models import *

# Register your models here.

admin.site.register(UserProfile)
#admin.site.register(Page)
#admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Notification)
