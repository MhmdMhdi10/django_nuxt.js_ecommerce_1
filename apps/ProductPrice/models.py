from apps.product.models import Product
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.core.models import BaseModel

domain = settings.DOMAIN


class PriceByUnit(BaseModel):
    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField()
    counting_unit = models.JSONField(_('counting_unit'), default={"en": "", "fa": ""})
