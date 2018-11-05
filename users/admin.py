from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserAvatar, Relationship

class AvatarInline(admin.StackedInline):
    model = UserAvatar

class MyUserAdmin(UserAdmin):
    inlines = (AvatarInline,)

admin.site.register(User, MyUserAdmin)
admin.site.register(UserAvatar)
admin.site.register(Relationship)
