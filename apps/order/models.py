import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel
from ecommerce.settings import AUTH_USER_MODEL
from apps.product.models import Product
from apps.coupon.models import Coupon


User = AUTH_USER_MODEL


class Order(BaseModel):

    class OrderStatus(models.TextChoices):
        NOT_PROCESSED = 'not_processed', _('Not processed')
        PROCESSED = 'processed', _('Processed')
        SHIPPING = 'shipped', _('Shipping')
        DELIVERED = 'delivered', _('Delivered')
        CANCELLED = 'cancelled', _('Cancelled')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='OrderItem')
    coupon = models.OneToOneField(Coupon, null=True, blank=True, on_delete=models.SET_NULL)
    transaction_id = models.CharField(max_length=255, unique=True)
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    shipping_name = models.CharField(max_length=255)
    shipping_price = models.IntegerField()
    shipping_time = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=50, choices=OrderStatus.choices, default=OrderStatus.NOT_PROCESSED)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def __str__(self):
        return f'{self.user.username} - {self.id}'


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    count = models.PositiveIntegerField(default=1)
    unit_price = models.IntegerField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')

    def __str__(self):
        return f'{self.order} - {self.product.name}'
