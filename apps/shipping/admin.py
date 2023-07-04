from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from apps.core.admin import BaseAdmin
from .models import Shipping


@admin.register(Shipping)
class ShippingAdmin(BaseAdmin):
    list_display = ('city', 'shipping_method', 'shipping_cost')
    list_filter = ('shipping_method',)
    search_fields = ('city', 'postal_code', 'address')
    fieldsets = (
        (None, {
            'fields': ('city', 'shipping_method', 'shipping_cost')
        }),
        (_('Additional Information'), {
            'classes': ('collapse',),
            'fields': ('postal_code', 'address', 'description')
        })
    )