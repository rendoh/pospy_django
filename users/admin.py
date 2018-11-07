from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, UsernameField
from .models import User, UserAvatar, Relationship

class AvatarInline(admin.StackedInline):
    model = UserAvatar

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)
        field_classes = {'username': UsernameField}

class MyUserAdmin(UserAdmin):
    inlines = (AvatarInline,)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'is_staff')
    search_fields = ('username', 'email')
    form = UserChangeForm
    add_form = MyUserCreationForm

admin.site.register(User, MyUserAdmin)
admin.site.register(UserAvatar)
admin.site.register(Relationship)
