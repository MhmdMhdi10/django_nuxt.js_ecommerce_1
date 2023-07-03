from django.contrib import admin
from apps.category.models import Category
from apps.core.admin import BaseAdmin


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('id', 'name', 'parent',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_display_links = ('name', 'parent')
    search_fields = ('name', 'parent')
    list_per_page = 25
