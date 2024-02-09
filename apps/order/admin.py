from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transaction_id', 'price', 'discount_price', 'shipping_name', 'shipping_price',
                    'shipping_time', 'status', 'is_paid',
                    'created_at', 'updated_at', 'deleted_at', 'created_by', 'updated_by', 'is_deleted']
    list_filter = ['status', 'is_paid']
    search_fields = ['user__username', 'transaction_id']
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'count', 'unit_price', 'date_added']
    list_filter = ['order']
    search_fields = ['order__user__username', 'product__name']
