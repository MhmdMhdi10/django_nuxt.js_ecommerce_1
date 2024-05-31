from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.admin import BaseAdmin
from .models import PriceByUnit
from apps.product.serializers import ProductSerializer


@admin.register(PriceByUnit)
class CouponAdmin(BaseAdmin):
    list_display = ('id', 'product', 'price', 'counting_unit',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('product',)
    search_fields = ('product',)
