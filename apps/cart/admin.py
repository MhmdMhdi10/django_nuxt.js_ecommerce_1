from django.contrib import admin
from .models import Cart, CartItem
from apps.core.admin import BaseAdmin


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1


class CartAdmin(BaseAdmin):
    list_display = ('id', 'user',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    inlines = (CartItemInline,)


class CartItemAdmin(BaseAdmin):
    list_display = ('id', 'cart', 'product', 'count',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('cart', 'product')


admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
