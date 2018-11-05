from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAvatar, Relationship

admin.site.register(User, UserAdmin)
admin.site.register(UserAvatar)
admin.site.register(Relationship)
