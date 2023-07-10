from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.admin import BaseAdmin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(BaseAdmin):
    list_display = ('code', 'type', 'discount', 'discount_amount', 'expire_date',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted')
    list_filter = ('type',)
    search_fields = ('code',)
    fieldsets = (
        (None, {
            'fields': ('code', 'type', 'expire_date')
        }),
        (_('Discount'), {
            'fields': ('discount', 'discount_amount'),
            'classes': ('collapse',)
        }),
    )

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')
