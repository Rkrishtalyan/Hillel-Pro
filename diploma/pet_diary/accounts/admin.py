from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = (
        'id', 'email', 'first_name', 'last_name',
        'phone_number', 'telegram_id', 'communication_method',
        'preferred_language', 'preferred_timezone', 'is_staff', 'is_superuser'
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'first_name', 'last_name', 'phone_number',
                'avatar',
                'telegram_id',
                'communication_method',
                'preferred_language',
                'preferred_timezone'
            )
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name',
                'phone_number', 'avatar',
                'telegram_id',
                'communication_method',
                'preferred_language',
                'preferred_timezone',
                'password1', 'password2',
                'is_staff', 'is_superuser'
            )}
         ),
    )

    ordering = ('email',)
