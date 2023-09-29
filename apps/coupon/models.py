from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.core.models import BaseModel


class Coupon(BaseModel):
    TYPE_PERCENTAGE = 'percentage'
    TYPE_PRICE = 'price'
    TYPE_CHOICES = [
        (TYPE_PERCENTAGE, _('Percentage')),
        (TYPE_PRICE, _('Price')),
    ]

    code = models.CharField(_('code'), max_length=50, unique=True)
    coupon_type = models.CharField(_('type'), max_length=20, choices=TYPE_CHOICES, default=TYPE_PERCENTAGE)
    coupon_value = models.IntegerField()
    expire_date = models.DateTimeField(_('expiration date'))

    class Meta:
        verbose_name = _('Coupon')
        verbose_name_plural = _('Coupons')

    def __str__(self):
        return self.code


