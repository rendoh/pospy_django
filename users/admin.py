from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('avatar',)
        }),
    )

admin.site.register(User, MyUserAdmin)
