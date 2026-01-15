from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = ('email', 'username', 'first_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    ordering = ('email',)
    search_fields = ('email', 'username', 'first_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'username')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    filter_horizontal = ('groups', 'user_permissions')
