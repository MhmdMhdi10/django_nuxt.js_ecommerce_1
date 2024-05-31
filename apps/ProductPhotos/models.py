from apps.product.models import Product
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from apps.core.models import BaseModel

domain = settings.DOMAIN


class ProductPhoto(BaseModel):
    class Meta:
        verbose_name = 'ProductPhoto'
        verbose_name_plural = 'ProductPhoto'

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%m/')
