from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.admin import BaseAdmin
from django.contrib.auth import get_user_model

from apps.user.models import OtpCode

User = get_user_model()


class UserAccountAdmin(BaseAdmin, admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    search_fields = ('username', 'phone_number')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('phone_number',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'phone_number', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(User, UserAccountAdmin)


class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')
    search_fields = ('phone_number', 'code')
    ordering = ('-created',)


admin.site.register(OtpCode, OtpCodeAdmin)
