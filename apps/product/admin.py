from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product
from apps.core.admin import BaseAdmin


class ProductAdmin(BaseAdmin):
    list_display = ('id', 'name', 'category', 'price', 'count', 'sold', 'discount_type', 'discount_value',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('category', 'created_at', 'updated_at', 'is_deleted')
    list_editable = ['price']
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'


admin.site.register(Product, ProductAdmin)
