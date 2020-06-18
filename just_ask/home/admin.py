from django.contrib import admin
from home.models import UserProfile,Question,Answer,Notification

admin.site.register(UserProfile)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Notification)

