from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Product, ProductDiscount
from apps.core.admin import BaseAdmin


class ProductAdmin(BaseAdmin):
    list_display = ('id', 'name', 'category', 'price', 'count', 'sold', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('category', 'created_at', 'updated_at', 'is_deleted')
    list_editable = ['price']
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'


class ProductDiscountAdmin(BaseAdmin):
    list_display = ('id', 'product', 'type', 'value', 'created_at', 'updated_at', 'is_deleted')
    list_filter = ('product', 'type', 'created_at', 'updated_at', 'is_deleted')
    list_editable = ['value']
    search_fields = ('product__name',)
    date_hierarchy = 'created_at'


admin.site.register(ProductDiscount, ProductDiscountAdmin)
admin.site.register(Product, ProductAdmin)
