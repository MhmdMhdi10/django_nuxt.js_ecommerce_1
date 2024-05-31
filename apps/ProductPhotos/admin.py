from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.admin import BaseAdmin
from .models import ProductPhoto
from apps.product.serializers import ProductSerializer


@admin.register(ProductPhoto)
class CouponAdmin(BaseAdmin):
    list_display = ('id', 'product', 'photo',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('product',)
    search_fields = ('product',)
