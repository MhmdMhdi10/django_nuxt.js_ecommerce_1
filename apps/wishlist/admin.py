from django.contrib import admin
from apps.core.admin import BaseAdmin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(BaseAdmin):
    list_display = ('user', 'product_count', 'created_at',)
    search_fields = ('user__username',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Product Count'
