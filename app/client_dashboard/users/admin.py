from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',
                    'is_admin', 'is_editor',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_admin','is_editor',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1',
                       'password2', 'is_staff', 'is_active', 'is_admin',
                       'is_editor',)}
         ),
    )
    search_fields = ('full_name', 'email',)
    ordering = ('full_name', 'email',)


admin.site.register(CustomUser, CustomUserAdmin)
