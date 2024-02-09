from django.contrib import admin
from apps.core.admin import BaseAdmin
from .models import Wishlist, WishlistItem


@admin.register(Wishlist)
class WishlistAdmin(BaseAdmin):
    list_display = ('user', 'product_count',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    search_fields = ('user__username',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Product Count'


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'created_at', 'updated_at',
                    'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('wishlist', 'product', 'created_at', 'updated_at',
                   'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    search_fields = ('wishlist__user__username', 'product__name')
    list_per_page = 20
