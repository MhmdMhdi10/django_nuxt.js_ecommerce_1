from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class BaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        obj.save()

    def logical_delete(self, request, queryset):
        queryset.update(deleted_at=timezone.now())
        queryset.update(is_deleted=True)

    def undelete(self, request, queryset):
        queryset.update(is_deleted=False)
        queryset.update(deleted_at=None)

    def hard_delete(self, request, queryset):
        for obj in queryset:
            obj.hard_delete()

    logical_delete.short_description = _('Logical delete selected %(verbose_name_plural)s')
    undelete.short_description = _('Undelete selected %(verbose_name_plural)s')
    hard_delete.short_description = _('Hard delete selected %(verbose_name_plural)s')

    actions = ['logical_delete', 'deactivate', 'activate', 'undelete', 'hard_delete']
