from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.admin import BaseAdmin
from .models import UserProfile, Address


@admin.register(UserProfile)
class UserProfileAdmin(BaseAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'image',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    search_fields = ('id', 'user__username', 'first_name', 'last_name')
    fields = ('user', 'image', 'first_name', 'last_name')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'user_profile']
        else:
            return ['id']


@admin.register(Address)
class AddressAdmin(BaseAdmin):
    list_display = ('id', 'user_profile', 'body', 'city',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    search_fields = ('id', 'user_profile__user__username', 'body', 'city')
    fields = ('user_profile', 'body', 'city')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['id', 'user_profile']
        else:
            return ['id']
