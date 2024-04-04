from django.contrib import admin
from apps.brand.models import Brand
from apps.core.admin import BaseAdmin


@admin.register(Brand)
class BrandAdmin(BaseAdmin):
    list_display = ('id', 'name', 'country', 'picture', 'description', 'file', 'file_2',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_display_links = ('name', 'description', 'country')
    search_fields = ('name', 'description', 'country')
    list_per_page = 25
